from django.shortcuts import redirect, render

# Create your views here.
import os
from rest_framework.views import APIView
from django.db import transaction
from datetime import datetime
import sys
from REMS import ins_logger, settings
from property.models import PropertyMaster, PropertyUnitDetails
from tenant_system.models import TenantDetails
import json
import uuid
from django.core.files.storage import FileSystemStorage
from django.core.paginator import Paginator


class TenantList(APIView):
    def get(self,request):

        try:

            ins_tenant = TenantDetails.objects.filter(int_status = 1 ).values('pk_bint_id','vchr_name','vchr_address','json_proofs_doc')
            lst_tenant = []
            for itr_pro in ins_tenant:
                dct_tenant = {}
                ins_units = PropertyUnitDetails.objects.filter(int_status = 1, fk_tenant_id = itr_pro['pk_bint_id']).values('fk_property_id','dbl_rent','fk_unit_types_id','fk_unit_types_id__vchr_name','fk_tenant_id','dat_agreement_end','dat_rent_payout','fk_property_id__vchr_name').first()

                dct_tenant['pk_bint_id'] = itr_pro['pk_bint_id']
                dct_tenant['vchr_name'] = itr_pro['vchr_name']
                dct_tenant['vchr_address'] = itr_pro['vchr_address']
                dct_tenant['json_proofs_doc'] = itr_pro['json_proofs_doc']
                dct_tenant['lst_units'] = ins_units

                lst_tenant.append(dct_tenant)
            paginator = Paginator(lst_tenant, 4)  # Display 2 records per page
            page_number = request.GET.get('page')
            lst_tent = paginator.get_page(page_number)
            # return Response({'status':1,'data':lst_tenant})
            return render(request, "add_tenant.html", {'data':lst_tent})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return render(request, "add_tenant.html", {'error_message':'Oops! Something Went Wrong'})


class AddTenant(APIView):

    def post(self,request):

        try:
            with transaction.atomic():
                if not request.data.get('str_name'):
                    return render(request, "create_tenant.html", {'error_message':'Please Enter Madatory Fields'})
                if not request.data.get('str_address'):
                    return render(request, "create_tenant.html", {'error_message':'Please Enter Madatory Fields'})

                # if len(request.data.get('lst_docs_names')) == 0:
                #     return Response({'status':0,'reason':'Please Upload Atleast 1 proof'})
                
                

                lst_doc_names = json.loads(request.data.get('lst_docs_names')) if request.data.get('lst_docs_names') else []
                lst_sketches = []
                for itr_names in lst_doc_names:
                    dct_docs = {}
                    str_doc_path = ""
                    if request.data.get(itr_names):
                        if not os.path.exists(settings.MEDIA_ROOT + '/tenant_docs/'):
                            os.mkdir(settings.MEDIA_ROOT + '/tenant_docs/')
                        doc_sketch = request.data.get(itr_names)
                        str_extension = doc_sketch.name.split('.')[1]
                        str_rename = str('id_')+uuid.uuid4().hex + '.' + str_extension
                        fs = FileSystemStorage(
                            location=settings.MEDIA_ROOT+'/tenant_docs', base_url=settings.MEDIA_URL+'tenant_docs/')
                        str_sketch = fs.save(str_rename, doc_sketch)
                        str_doc_path = fs.url(str_sketch)
                        dct_docs['Remark'] = doc_sketch.name 
                        dct_docs['Pathdoc'] = str_doc_path
                        lst_sketches.append(dct_docs)
                    
                if request.data.get('image'):
                    if not os.path.exists(settings.MEDIA_ROOT + '/tenant_docs/'):
                        os.mkdir(settings.MEDIA_ROOT + '/tenant_docs/')
                    doc_sketch = request.data.get('image')
                    str_extension = doc_sketch.name.split('.')[1]
                    str_rename = str('id_')+uuid.uuid4().hex + '.' + str_extension
                    fs = FileSystemStorage(
                        location=settings.MEDIA_ROOT+'/tenant_docs', base_url=settings.MEDIA_URL+'tenant_docs/')
                    str_sketch = fs.save(str_rename, doc_sketch)
                    str_doc_path = fs.url(str_sketch)
                    # dct_docs['Remark'] = doc_sketch.name 
                    # dct_docs['Pathdoc'] = str_doc_path
                    lst_sketches.append(str_doc_path)
                ins_tenant = TenantDetails.objects.create(
                        vchr_name = request.data.get('str_name'),
                        vchr_address = request.data.get('str_address'),
                        int_status = 1,
                        fk_created_id = request.user.id,
                        dat_created = datetime.now(),
                        json_proofs_doc = lst_sketches
                )

                ins_units = PropertyUnitDetails.objects.filter(pk_bint_id = request.data.get('int_unit_id')).update(
                        fk_tenant_id = ins_tenant.pk_bint_id,
                        dat_agreement_end = datetime.strptime(request.data.get('dat_end') , '%m/%d/%Y').strftime('%Y-%m-%d'),
                        dat_rent_payout =  datetime.strptime(request.data.get('dat_rent'), '%m/%d/%Y').strftime('%Y-%m-%d'),
                        fk_updated_id = request.user.id,
                        dat_updated = datetime.now()
                    )

                    

                return redirect('/tenant/tenant_list')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return render(request, "create_tenant.html", {'error_message':'Oops! Something Went Wrong'})


    def get(self,request):

        try:

            ins_units = PropertyUnitDetails.objects.filter(int_status = 1).values('fk_property_id','dbl_rent','fk_unit_types_id','fk_unit_types_id__vchr_name','fk_tenant_id','dat_agreement_end','dat_rent_payout','fk_property_id__vchr_name','pk_bint_id')

            return render(request, "create_tenant.html", {'lst_units':ins_units})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return render(request, "create_tenant.html", {'error_message':'Oops! Something Went Wrong'})

class ViewTenant(APIView):
    def get(self,request,id):

        try:

            ins_tenant = TenantDetails.objects.filter(pk_bint_id = id).values('pk_bint_id','vchr_name','vchr_address','json_proofs_doc').first()

            ins_units = PropertyUnitDetails.objects.filter(int_status = 1, fk_tenant_id = ins_tenant['pk_bint_id']).values('fk_property_id','dbl_rent','fk_unit_types_id','fk_unit_types_id__vchr_name','fk_tenant_id','dat_agreement_end','dat_rent_payout','fk_property_id__vchr_name').first()



            return render(request, "view_tenant.html", {'ins_tenant':ins_tenant,'ins_units':ins_units})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return render(request, "view_tenant.html", {'error_message':'Oops! Something Went Wrong'})
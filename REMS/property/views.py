from django.shortcuts import render, redirect
from rest_framework.views import APIView
from django.db import transaction
from datetime import datetime
from rest_framework.response import Response
import sys
from REMS import ins_logger
import json
from property.models import PropertyMaster, PropertyUnitDetails, UnitTypes
# Create your views here.
from django.core.paginator import Paginator


class PropertyList(APIView):
    def get(self,request):

        try:
   
            ins_property = PropertyMaster.objects.filter(int_status = 1 ).values('pk_bint_id','vchr_name','vchr_address','vchr_location','txt_features')
            
            paginator = Paginator(ins_property, 4)  # Display 4 records per page
            page_number = request.GET.get('page')
            lst_courses = paginator.get_page(page_number)
            return render(request, "add_property.html", {'data':lst_courses})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return Response({'status':0,'message':str(e)+ ' in Line No: '+str(exc_tb.tb_lineno)})


class AddProperty(APIView):

    def post(self,request):

        try:
            with transaction.atomic():
                if not request.data.get('str_name'):
                    
                    return render(request, "create_property.html", {'error_message':'Please Enter Madatory Fields'})
                if not request.data.get('str_address'):
                   
                    return render(request, "create_property.html", {'error_message':'Please Enter Madatory Fields, Enter Address'})
                if not request.data.get('str_location'):
                    
                    return render(request, "create_property.html", {'error_message':'Please Enter Madatory Fields, Enter Location'})
                if not request.data.get('str_features'):
                    
                    return render(request, "create_property.html", {'error_message':'Please Enter Madatory Fields, Enter Features'})
                # if len(request.data.get('lst_units')) == 0:
                #     return Response({'status':0,'reason':'Please Enter Atleast 1 Unit Details'})
                
                ins_property = PropertyMaster.objects.create(
                        vchr_name = request.data.get('str_name'),
                        vchr_address = request.data.get('str_address'),
                        vchr_location = request.data.get('str_location'),
                        txt_features = request.data.get('str_features'),
                        int_status = 1,
                        fk_created_id = request.user.id,
                        dat_created = datetime.now()
                )

                # lst_units = request.data.get('lst_units') if request.data.get('lst_units') and len(request.data.get('lst_units')) > 0 else []

                #  lst_unit_selected_json = request.POST.get('lst_unit_selected')
                # lst_unit_selected = json.loads(lst_unit_selected_json)
                
                # for entry in lst_unit_selected:
                ins_units = PropertyUnitDetails.objects.create(
                        fk_property_id = ins_property.pk_bint_id,
                        dbl_rent = request.data.get('dbl_rent'),
                        fk_unit_types_id = request.data.get('int_unit'),
                        int_status = 1,
                        fk_created_id = request.user.id,

                    )

                
                
                lst_unit_selected_json = request.POST.get('lst_unit_selected')
                lst_unit_selected = json.loads(lst_unit_selected_json)
                if lst_unit_selected and len(lst_unit_selected) == 0:
                    return render(request, "create_property.html", {'error_message':'Please Enter unit details correctly'})
                
                for index,itr_unit in enumerate(lst_unit_selected):


                    ins_units = PropertyUnitDetails.objects.create(
                        fk_property_id = ins_property.pk_bint_id,
                        dbl_rent = itr_unit['dbl_rent'],
                        fk_unit_types_id = itr_unit['int_unit'],
                        int_status = 1,
                        fk_created_id = request.user.id,

                    )
                    

                return redirect('/property/property_list')
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return render(request, "create_property.html", {'error_message': 'Oops! Something Went Wrong'})


    def get(self,request):

        try:

            ins_units = UnitTypes.objects.filter(int_status = 1).values('vchr_name','vchr_code','pk_bint_id')
            lst_unit_selected = []
            dct_selec = {'dbl_rent': None,'int_unit': None}
            return render(request, "create_property.html", {'lst_units':ins_units, 'lst_unit_selected':lst_unit_selected , 'dct_selec':dct_selec})
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return render(request, "create_property.html", {'error_message': 'Oops! Something Went Wrong'})


class ViewProperty(APIView):
    def get(self, request, id):
        try:
            ins_property = PropertyMaster.objects.filter(pk_bint_id = id ).values('pk_bint_id','vchr_name','vchr_address','vchr_location','txt_features').first()
            ins_units = PropertyUnitDetails.objects.filter(int_status =1, fk_property_id = ins_property['pk_bint_id']).values('fk_property_id','dbl_rent','fk_unit_types_id','fk_unit_types_id__vchr_name','fk_tenant_id','fk_tenant_id__vchr_name','dat_agreement_end','dat_rent_payout')

            return render(request, "view_property.html", {'ins_property': ins_property,'ins_units':ins_units})
        
        except Exception as e:
            exc_type, exc_obj, exc_tb = sys.exc_info()
            ins_logger.logger.error(e,extra={'details':'line no: ' + str(exc_tb.tb_lineno),'user': 'user_id:' + str(request.user.id)})
            return render(request, "view_property.html", {'error_message': 'Oops! Something Went Wrong'})
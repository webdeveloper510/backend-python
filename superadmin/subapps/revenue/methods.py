from superadmin.subapps.media_and_groupings import models as models_media
from datetime import datetime, timedelta
from superadmin.subapps.receipt import models as models_receipt
from rest_framework import serializers

# Method
def compute_subscription_revenue(type, objs, first_date, last_date, city, country):
    subscription_types = ["ADVANCED", "PREMIUM", "ENTERPRISE", "CUSTOM", "BASIC"]
    rc = models_receipt.ReceiptConfig.objects.filter(city__country__name=country)
    if city:
        rc = rc.filter(city=city)

    if(not rc.exists()):
        raise serializers.ValidationError({"error":"given city has no receipt configuration for Tax. please configure receipt for this city first."})
    # tax_rate = rc.first().tax_rate
    tax_name = rc.first().tax_name
    # tax_rate = city.
    if(type == "TIME_BASED"): # Calculate TIME_BASED Revenue
        resp_objs = []
        for st in subscription_types:
            current_objs = objs.filter(subscription__subscription_type=st, total_amount_paid__isnull=False )
            if first_date:
                current_objs = current_objs.filter(start_date__gt = first_date - timedelta(days=1), start_date__lt = last_date + timedelta(days=1))
            gross_revenue = 0
            tax = 0
            for obj in current_objs:
                if(obj.total_amount_paid):
                    gross_revenue += obj.total_amount_paid
                    if(obj.applied_tax_rate):
                        tax += obj.total_amount_paid - (obj.total_amount_paid/(1+(obj.applied_tax_rate/100) ) )
            # print(gross_revenue)
            resp_objs.append({
                "subscription_type":st,
                "gross_revenue":gross_revenue,
                # "tax_name":tax_name,
                "tax":tax,
                "net_revenue": gross_revenue - tax,
                "number_of_subscriptions": current_objs.count() ,
                "average_subscription": round(gross_revenue/current_objs.count()) if current_objs.count()!=0 else 0 ,
            })

    else:   # Calculate ACCOUNTING Revenue
        resp_objs = []
        
        for st in subscription_types:
            
            current_objs = objs.filter(subscription__subscription_type=st, total_amount_paid__isnull=False )
            gross_revenue = 0
            tax = 0
            sub_count = 0
            for obj in current_objs:
                if not first_date:
                    today = datetime.today().date()
                    if(obj.start_date.date() <= today and obj.end_date.date() <= today): 
                        # When subscription is end
                        gross_revenue += obj.total_amount_paid
                        sub_count += 1
                    
                    elif(obj.start_date.date() <= today and obj.end_date.date() >= today): 
                        # when subscription is continue
                        total_days = obj.end_date.date()-obj.start_date.date()
                        diff = obj.end_date.date() - today + timedelta(days=1)
                        subsCrip_used = total_days - diff
                        per_day_amount = obj.get_daily_subscription_cost()
                        effective_amount = per_day_amount * subsCrip_used.days
                        gross_revenue += effective_amount
                        sub_count += 1
                

                else:
                    if(obj.start_date.date() >= first_date and obj.end_date.date() <= last_date): #start_date >= today & end_date <= today **** 
                        gross_revenue += obj.total_amount_paid
                        sub_count += 1
                    
                    elif(obj.start_date.date() <= first_date and obj.end_date.date() >= first_date and obj.end_date.date() <= last_date ):
                        diff = obj.end_date.date() - first_date + timedelta(days=1)
                        per_day_amount = obj.get_daily_subscription_cost()
                        effective_amount = per_day_amount * diff.days
                        gross_revenue += effective_amount
                        
                        sub_count += 1
                     
                    elif(obj.end_date.date() >= last_date and obj.start_date.date() >= first_date and obj.start_date.date() <= last_date ):
                        diff = last_date - obj.start_date.date() + timedelta(days=1)
                        per_day_amount = obj.get_daily_subscription_cost()
                        effective_amount = per_day_amount * diff.days
                        gross_revenue += effective_amount
                        sub_count += 1
                    
                    elif(obj.start_date.date() <= first_date and obj.end_date.date() >= last_date ):
                        diff = last_date - first_date + timedelta(days=1)
                        per_day_amount = obj.get_daily_subscription_cost()
                        effective_amount = per_day_amount * diff.days
                        gross_revenue += effective_amount
                        sub_count += 1
                        # if(obj.applied_tax_rate):
                        #     tax += effective_amount - (effective_amount/(1+(obj.applied_tax_rate/100) ) )
                
            
            resp_objs.append({
                "subscription_type":st,
                "gross_revenue":gross_revenue,
                "tax":tax,
                "net_revenue": gross_revenue - tax,
                "number_of_subscriptions": current_objs.count() ,
                "average_subscription": round(gross_revenue/current_objs.count()) if current_objs.count()!=0 else 0 ,
            })
    return resp_objs

def compute_advertising_revenue(type, objs, first_date, last_date):
    ad_types = dict(models_media.MARKETING_TYPE).keys()

    if(type == "TIME_BASED"): # Calculate TIME_BASED Revenue
        resp_objs = []
        for ad in ad_types:
            current_objs = objs.filter(type=ad, total_amount_paid__isnull=False )
            if first_date:
                current_objs = current_objs.filter(from_date__gt = first_date - timedelta(days=1), to_date__lt = last_date + timedelta(days=1))
            vendors = current_objs.values('vendor').distinct()
            gross_revenue = 0
            tax = 0
            for obj in current_objs:
                if(obj.total_amount_paid):
                    gross_revenue += obj.total_amount_paid
                    if(obj.applied_tax_rate):
                        tax += obj.total_amount_paid - (obj.total_amount_paid/(1+(obj.applied_tax_rate/100) ) )
            resp_objs.append({
                "ad_type":ad,
                "gross_revenue":gross_revenue,
                "tax":tax,
                "net_revenue": gross_revenue - tax,
                "number_of_unique_vendors": vendors.count() ,
                "average_revenue_per_day": round(gross_revenue/current_objs.count()) if current_objs.count()!=0 else 0 ,
            })

        
    else:   # Calculate ACCOUNTING Revenue
        resp_objs = []
        for ad in ad_types:
            current_objs = objs.filter(type=ad, total_amount_paid__isnull=False )
            if first_date:
                current_objs = current_objs.filter(from_date__gt = first_date - timedelta(days=1), to_date__lt = last_date + timedelta(days=1))
            
            gross_revenue = 0
            tax = 0
            sub_count = 0
            for obj in current_objs:
                if not first_date:
                    today = datetime.today().date()
                    if(obj.from_date <= today and obj.to_date <= today): 
                        # When subscription is end
                        gross_revenue += obj.total_amount_paid
                        if(obj.applied_tax_rate):
                            tax += obj.total_amount_paid - (obj.total_amount_paid/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1
                    
                    elif(obj.from_date <= today and obj.to_date >= today): 
                        # when subscription is continue
                        total_days = obj.to_date-obj.from_date
                        diff = obj.to_date - today + timedelta(days=1)
                        subsCrip_used = total_days - diff
                        per_day_amount = obj.get_daily_cost()
                        effective_amount = per_day_amount * subsCrip_used.days
                        gross_revenue += effective_amount
                        sub_count += 1
                        if(obj.applied_tax_rate):
                            tax += effective_amount - (effective_amount/(1+(obj.applied_tax_rate/100) ) )
                else:
                    if(obj.from_date >= first_date and obj.to_date <= last_date):
                        gross_revenue += obj.total_amount_paid
                        if(obj.applied_tax_rate):
                            tax += obj.total_amount_paid - (obj.total_amount_paid/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1

                        
                    # from_date = 2020/01/01 and to_date = 2020/12/31
                    # first_date = 2020/05/01 and last_date = 2021/01/01

                    # started already(from_date <= first_date) and (to_date >= first_date) and to_date <= last_date
                    elif(obj.from_date <= first_date and obj.to_date >= first_date and obj.to_date <= last_date ):
                        diff = obj.to_date - first_date + timedelta(days=1)
                        # per_day_amount = obj.total_amount_paid / (obj.end_date.date() - obj.start_date.date()  ).days
                        per_day_amount = obj.get_daily_cost()
                        effective_amount = per_day_amount * diff.days
                        gross_revenue += effective_amount
                        if(obj.applied_tax_rate):
                            tax += effective_amount - (effective_amount/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1
                    

                    # from_date = 2020/06/01 and to_date = 2021/05/31
                    # first_date = 2020/05/01 and last_date = 2021/01/01
                    # to_date >= last_date and from_date >= first_date and from_date <= last_date

                    elif(obj.to_date >= last_date and obj.from_date >= first_date and obj.from_date <= last_date ):
                        diff = last_date - obj.from_date + timedelta(days=1)
                        # per_day_amount = obj.total_amount_paid / (obj.end_date.date() - obj.start_date.date() + timedelta(days=1)).days
                        per_day_amount = obj.get_daily_cost()
                        effective_amount = per_day_amount * diff.days
                        gross_revenue += effective_amount
                        if(obj.applied_tax_rate):
                            tax += effective_amount - (effective_amount/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1

                    
                    # from_date = 2020/04/01 and to_date = 2021/05/31
                    # first_date = 2020/05/01 and last_date = 2021/01/01
                    # from_date <= first_date and to_date >= last_date
                    
                    elif(obj.from_date <= first_date and obj.to_date >= last_date ):
                        diff = last_date - first_date + timedelta(days=1)
                        per_day_amount = obj.get_daily_cost()
                        effective_amount = per_day_amount * diff.days
                        gross_revenue += effective_amount
                        if(obj.applied_tax_rate):
                            tax += effective_amount - (effective_amount/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1
                    
                
            vendors = current_objs.values('vendor').distinct()
            resp_objs.append({
                "ad_type":ad,
                "gross_revenue":gross_revenue,
                "tax":tax,
                "net_revenue": gross_revenue - tax,
                "number_of_unique_vendors": vendors.count() ,
                "average_revenue_per_day": round(gross_revenue/current_objs.count()) if current_objs.count()!=0 else 0 ,
            })
        
    return resp_objs



# Method
def compute_banner_marketing_revenue(type, objs, first_date, last_date):
    # subscription_types = ["ADVANCED", "PREMIUM", "ENTERPRISE", "CUSTOM"]
    categories = models_media.Category.objects.all().values_list('name', flat=True)
    if(type == "TIME_BASED"): # Calculate TIME_BASED Revenue
        resp_objs = []
        for cat in categories:
            current_objs = objs.filter(banner_details__catagory__name=cat, total_amount_paid__isnull=False )
            if first_date:
                current_objs = current_objs.filter(from_date__gt = first_date - timedelta(days=1), from_date__lt = last_date + timedelta(days=1))

            gross_revenue = 0
            tax = 0
            for obj in current_objs:
                if(obj.total_amount_paid):
                    gross_revenue += obj.total_amount_paid
                    if(obj.applied_tax_rate):
                        tax += obj.total_amount_paid - (obj.total_amount_paid/(1+(obj.applied_tax_rate/100) ) )
            resp_objs.append({
                "category":cat,
                "gross_revenue":gross_revenue,
                "tax":tax,
                "net_revenue": gross_revenue - tax,
                "number_of_unique_vendors": current_objs.count() ,
                "average_revenue_per_day": round(gross_revenue/current_objs.count()) if current_objs.count()!=0 else 0 ,
            })

        pass
    else:   # Calculate ACCOUNTING Revenue
        resp_objs = []
        for cat in categories:
            current_objs = objs.filter(banner_details__catagory__name=cat, total_amount_paid__isnull=False )
            gross_revenue = 0
            tax = 0
            sub_count = 0
            for obj in current_objs:
                print('*************', first_date)
                if not first_date:
                    today = datetime.today().date()
                    if(obj.from_date <= today and obj.to_date <= today): 
                        # When subscription is end
                        gross_revenue += obj.total_amount_paid
                        if(obj.applied_tax_rate):
                            tax += obj.total_amount_paid - (obj.total_amount_paid/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1
                    
                    elif(obj.from_date <= today and obj.to_date >= today): 
                        # when subscription is continue
                        total_days = obj.to_date-obj.from_date
                        diff = obj.to_date - today + timedelta(days=1)
                        subsCrip_used = total_days - diff
                        per_day_amount = obj.get_daily_cost()
                        effective_amount = per_day_amount * subsCrip_used.days
                        gross_revenue += effective_amount
                        sub_count += 1
                        if(obj.applied_tax_rate):
                            tax += effective_amount - (effective_amount/(1+(obj.applied_tax_rate/100) ) )

                else:         
                    if(obj.from_date >= first_date and obj.to_date <= last_date):
                        gross_revenue += obj.total_amount_paid
                        if(obj.applied_tax_rate):
                            tax += obj.total_amount_paid - (obj.total_amount_paid/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1
                    
                    elif(obj.from_date <= first_date and obj.to_date >= first_date and obj.to_date <= last_date ):
                        diff = obj.to_date - first_date + timedelta(days=1)
                        # per_day_amount = obj.total_amount_paid / (obj.end_date.date() - obj.start_date.date()  ).days
                        per_day_amount = obj.get_daily_cost()
                        effective_amount = per_day_amount * diff.days
                        gross_revenue += effective_amount
                        if(obj.applied_tax_rate):
                            tax += effective_amount - (effective_amount/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1
                    
                    elif(obj.to_date >= last_date and obj.from_date >= first_date and obj.from_date <= last_date ):
                        diff = last_date - obj.from_date + timedelta(days=1)
                        # per_day_amount = obj.total_amount_paid / (obj.end_date.date() - obj.start_date.date() + timedelta(days=1)).days
                        per_day_amount = obj.get_daily_cost()
                        effective_amount = per_day_amount * diff.days
                        gross_revenue += effective_amount
                        if(obj.applied_tax_rate):
                            tax += effective_amount - (effective_amount/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1
                    
                    elif(obj.from_date <= first_date and obj.to_date >= last_date ):
                        diff = last_date - first_date + timedelta(days=1)
                        per_day_amount = obj.get_daily_cost()
                        effective_amount = per_day_amount * diff.days
                        gross_revenue += effective_amount
                        if(obj.applied_tax_rate):
                            tax += effective_amount - (effective_amount/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1
                
                pass
            
            resp_objs.append({
                "category":cat,
                "gross_revenue":gross_revenue,
                "tax":tax,
                "net_revenue": gross_revenue - tax,
                "number_of_unique_vendors": current_objs.count() ,
                "average_revenue_per_day": round(gross_revenue/current_objs.count()) if current_objs.count()!=0 else 0 ,
            })
        pass
    return resp_objs


# Method
def compute_search_word_marketing_revenue(type, objs, first_date, last_date):
    # subscription_types = ["ADVANCED", "PREMIUM", "ENTERPRISE", "CUSTOM"]
    word_count = models_media.SearchWordPricing.objects.all().values_list('no_of_searchwords', flat=True).distinct()
    
    if(type == "TIME_BASED"): # Calculate TIME_BASED Revenue
        resp_objs = []
        for wc in word_count:
                
            current_objs = objs.filter(searchword_details__no_of_searchwords=wc, total_amount_paid__isnull=False )
            if first_date:
                current_objs = current_objs.filter(from_date__gt = first_date - timedelta(days=1), from_date__lt = last_date + timedelta(days=1))
            gross_revenue = 0
            tax = 0
            for obj in current_objs:
                if(obj.total_amount_paid):
                    gross_revenue += obj.total_amount_paid
                    if(obj.applied_tax_rate):
                        tax += obj.total_amount_paid - (obj.total_amount_paid/(1+(obj.applied_tax_rate/100) ) )
            
            resp_objs.append({
                "word_count":wc,
                "gross_revenue":gross_revenue,
                "tax":tax,
                "net_revenue": gross_revenue - tax,
                "number_of_unique_vendors": current_objs.count() ,
                "average_revenue_per_day": round(gross_revenue/current_objs.count()) if current_objs.count()!=0 else 0 ,
            })

        
    else:   # Calculate ACCOUNTING Revenue
        resp_objs = []
        for wc in word_count:
            current_objs = objs.filter(searchword_details__no_of_searchwords=wc, total_amount_paid__isnull=False )
            gross_revenue = 0
            tax = 0
            sub_count = 0
            for obj in current_objs:

                if not first_date:
                    today = datetime.today().date()
                    if(obj.from_date <= today and obj.to_date <= today): 
                        # When subscription is end
                        gross_revenue += obj.total_amount_paid
                        if(obj.applied_tax_rate):
                            tax += obj.total_amount_paid - (obj.total_amount_paid/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1
                    
                    elif(obj.from_date <= today and obj.to_date >= today): 
                        # when subscription is continue
                        total_days = obj.to_date-obj.from_date
                        diff = obj.to_date - today + timedelta(days=1)
                        subsCrip_used = total_days - diff
                        per_day_amount = obj.get_daily_cost()
                        effective_amount = per_day_amount * subsCrip_used.days
                        gross_revenue += effective_amount
                        sub_count += 1
                        if(obj.applied_tax_rate):
                            tax += effective_amount - (effective_amount/(1+(obj.applied_tax_rate/100) ) )

                else:
                    if(obj.from_date >= first_date and obj.to_date <= last_date):
                        gross_revenue += obj.total_amount_paid
                        if(obj.applied_tax_rate):
                            tax += obj.total_amount_paid - (obj.total_amount_paid/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1
                    
                    elif(obj.from_date <= first_date and obj.to_date >= first_date and obj.to_date <= last_date ):
                        diff = obj.to_date - first_date + timedelta(days=1)
                        # per_day_amount = obj.total_amount_paid / (obj.end_date.date() - obj.start_date.date()  ).days
                        per_day_amount = obj.get_daily_cost()
                        effective_amount = per_day_amount * diff.days
                        gross_revenue += effective_amount
                        if(obj.applied_tax_rate):
                            tax += effective_amount - (effective_amount/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1
                    
                    elif(obj.to_date >= last_date and obj.from_date >= first_date and obj.from_date <= last_date ):
                        diff = last_date - obj.from_date + timedelta(days=1)
                        # per_day_amount = obj.total_amount_paid / (obj.end_date.date() - obj.start_date.date() + timedelta(days=1)).days
                        per_day_amount = obj.get_daily_cost()
                        effective_amount = per_day_amount * diff.days
                        gross_revenue += effective_amount
                        if(obj.applied_tax_rate):
                            tax += effective_amount - (effective_amount/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1
                    
                    elif(obj.from_date <= first_date and obj.to_date >= last_date ):
                        diff = last_date - first_date + timedelta(days=1)
                        per_day_amount = obj.get_daily_cost()
                        effective_amount = per_day_amount * diff.days
                        gross_revenue += effective_amount
                        if(obj.applied_tax_rate):
                            tax += effective_amount - (effective_amount/(1+(obj.applied_tax_rate/100) ) )
                        sub_count += 1
            
            resp_objs.append({
                "word_count":wc,
                "gross_revenue":gross_revenue,
                "tax":tax,
                "net_revenue": gross_revenue - tax,
                "number_of_unique_vendors": current_objs.count() ,
                "average_revenue_per_day": round(gross_revenue/current_objs.count()) if current_objs.count()!=0 else 0 ,
            })
        pass
    return resp_objs

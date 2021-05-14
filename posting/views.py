import json
import bcrypt

from django.views          import View
from django.http           import JsonResponse
from django.core.paginator import Paginator

from .models               import Posting
from .utils                import get_client_ip

class PostingView(View):
    def post(self,request):
        try:
            data     = json.loads(request.body)
            title    = data['title']
            name     = data['name']
            password = data['password']
            contents = data['contents']

            if len(password) < 4:
                return JsonResponse({'MESSAGE' : 'INVALID PASSWORD'},status = 400)
            
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

            Posting.objects.create(
                title    = title,
                name     = name,
                password = hashed_password,
                contents = contents
            )
            return JsonResponse({'MESSAGE' : 'SUCCESS'},status = 201)
        
        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE ERROR'}, status = 400)

    def get(self,request,posting_id):
        try:
            posting = Posting.objects.get(id=posting_id)
            posting_detail = [{
                'id'       : posting.id,
                'name'     : posting.name,
                'title'    : posting.title,
                'contents' : posting.contents,
                'user_ip'  : get_client_ip(request)
            }]

            return JsonResponse({'DETAIL' : posting_detail},status= 200)
        except Posting.DoesNotExist:
            return JsonResponse({'MESSAGE': 'POSTING_DOES_NOT_EXIST'},status= 404)

    def patch(self,request,posting_id):
        try:
            data     = json.loads(request.body)
            posting  = Posting.objects.get(id=posting_id)
            contents = data.get('contents',posting.contents)
            title    = data.get('title',posting.title)

            Posting.objects.filter(id=posting_id).update(
                contents = contents,
                title    = title
            )
            return JsonResponse({'MESSAGE' : 'SUCCESS'},status = 201)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE ERROR'}, status = 400)
        except Posting.DoesNotExist:
            return JsonResponse({'MESSAGE': 'POSTING_DOES_NOT_EXIST'},status= 404)
    
    def delete(self,request,posting_id):
        try:
            Posting.objects.get(id=posting_id).delete()

            return JsonResponse({'MESSAGE' : 'SUCCESS'},status = 201)

        except Posting.DoesNotExist:
            return JsonResponse({'MESSAGE': 'POSTING_DOES_NOT_EXIST'},status= 404)

class PasswordCheckView(View):
    def post(self,request,posting_id):
        try:
            data     = json.loads(request.body)
            post     = Posting.objects.get(id=posting_id)
            password = bcrypt.checkpw(data['password'].encode('utf-8'), post.password.encode('utf-8'))

            if not password:
                return JsonResponse({'MESSAGE' : 'CHECK YOUR PASSWORD'},status=400)

            return JsonResponse({'MESSAGE' : 'SUCCESS'},status= 200)

        except KeyError:
            return JsonResponse({'MESSAGE' : 'KEY ERROR'}, status = 400)
        except ValueError:
            return JsonResponse({'MESSAGE' : 'VALUE ERROR'}, status = 400)   
        except Posting.DoesNotExist:
            return JsonResponse({'MESSAGE': 'POSTING_DOES_NOT_EXIST'},status= 404)         

class PostingListView(View):
    def get(self,request):
        try:
            page             = request.GET.get('page',1)
            paginator        = Paginator(Posting.objects.all(),16)
            posting_zip      = paginator.get_page(page)
            posting_list     = [{
                'id'         : posting.id,
                'title'      : posting.title,
                'created_at' : posting.created_at,
                'updated_at' : posting.updated_at,
                'name'       : posting.name,
                'user_ip'    : get_client_ip(request)
            } for posting in posting_zip]

            return JsonResponse({'POSTING_LIST': posting_list},status=200)

        except Posting.DoesNotExist:
            return JsonResponse({'MESSAGE': 'POSTING_DOES_NOT_EXIST'},status= 404)
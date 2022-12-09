from django.conf import settings
import stripe
from django.shortcuts import render, reverse, redirect
import os
import openai


openai.api_key = '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'
# Create your views here.


def generatesocialmediacaptions(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Write a 10 different  Social media Captions on the topic of:{}\n".format(
            prompt),
        temperature=0.7,
        max_tokens=1073,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    result = response['choices'][0]['text']
    return result


def generatepoems(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Write a Poem on the topic of:{}\n\n".format(prompt),
        temperature=0.7,
        max_tokens=1073,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    result = response['choices'][0]['text']

    return result


def generatearticle(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate a 500 word  article on the topic of:{}\n\n".format(
            prompt),
        temperature=0.7,
        max_tokens=1119,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )

    result = response['choices'][0]['text']
    return result


def generateshortstory(prompt):
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt="Generate a 1000 word short story on the topic of :{}\n".format(
            prompt),
        temperature=0.7,
        max_tokens=3311,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    result = response['choices'][0]['text']
    return result


# def create_checkout_session():
#   session = stripe.checkout.Session.create(
#     line_items=[{
#       'price_data': {
#         'currency': 'usd',
#         'product_data': {
#           'name': 'T-shirt',
#         },
#         'unit_amount': 2000,
#       },
#       'quantity': 1,
#     }],
#     mode='payment',
#     success_url='http://localhost:4242/success',
#     cancel_url='http://localhost:4242/cancel',
#   )

#   return redirect(session.url, code=303)

# def payment(request,result,content_type,prompt):
#   stripe.api_key = settings.STRIPE_SECRET_KEY

#   session = stripe.checkout.Session.create(
#               line_items=[{
#                 'price':'price_1MCQ35KWEumvZSLC5QeSAZsR',
#                 'quantity': 1,
#               }],
#               mode='payment',
#             #   success_url=request.build_absolute_uri(reverse('result',))+'?session_id={CHECKOUT_SESSION_ID}',
#               success_url=request.build_absolute_uri(redirect('result',kwargs={'result':result,'content_type':content_type,'prompt':prompt, }))+'?session_id={CHECKOUT_SESSION_ID}',
#               cancel_url=request.build_absolute_uri(reverse('home')),
#     )
#   return session


def home(request):
    stripe.api_key = settings.STRIPE_SECRET_KEY
    session = stripe.checkout.Session.create(
        line_items=[{
            'price': 'price_1MCQ35KWEumvZSLC5QeSAZsR',
            'quantity': 1,
        }],
        mode='payment',
        #   success_url=request.build_absolute_uri(reverse('result',))+'?session_id={CHECKOUT_SESSION_ID}',
        success_url=request.build_absolute_uri(
            reverse('result'))+'?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('home')),
    )
    if request.method == 'POST':
        prompt = request.POST['describe']
        content_type = request.POST['content_type']
        content_type = int(content_type)
        request.session['content_type'] = content_type
        request.session['prompt'] = prompt
        print(content_type,">>>")
        if content_type == 1:
            result = generatearticle(prompt)
            # print(result)
            request.session['result'] = result
            return render(request, 'result.html')
        elif content_type == 2:
            result = generatesocialmediacaptions(prompt)
            # 'content_type'=content_type, 'prompt': prompt
            # context={'result': result, 'content_type': content_type, 'prompt': prompt}
            # print(context)
            # request.session['result'] = result
            request.session['result'] = result
           
            # print(request.session['result'],"Sessions")
            # return redirect('result/?result='+result+'&content_type='+str(content_type)+'&prompt='+prompt)
            return render(request, 'result.html')
        elif content_type == 3:
            result = generateshortstory(prompt)
            request.session['result'] = result
    
            return render(request, 'result.html', {'result': result, 'content_type': content_type, 'prompt': prompt})
        elif content_type == 4:
            result = generatepoems(prompt)
            request.session['result'] = result
            return render(request, 'result.html', {'result': result, 'content_type': content_type, 'prompt': prompt})

    else:

        return render(request, 'home.html', {'session_id': session.id, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY})


def result(request):

    stripe.api_key = settings.STRIPE_SECRET_KEY

    session = stripe.checkout.Session.create(
        line_items=[{
            'price': 'price_1MCQ4RKWEumvZSLCP7jBe74l',
            'quantity': 1,
        }],
        mode='payment',
        success_url=request.build_absolute_uri(
            reverse('result'))+'?session_id={CHECKOUT_SESSION_ID}',
        cancel_url=request.build_absolute_uri(reverse('result')),
    )
    # 'content_type': content_type, 'prompt': prompt
    ctx = {'result':  request.session['result'],'content_type': request.session.get('content_type'),'prompt': request.session.get('prompt'),'session_id': session.id, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY}
    if request.method == 'POST':
        prompt = request.POST['describe']
        content_type = request.POST.get('content_type')
        content_type = int(content_type)
        print(content_type)
        request.session['content_type'] = content_type
        request.session['prompt'] = prompt
        if content_type == 1:
            result = generatearticle(prompt)
            request.session['result'] = result
            return render(request, 'result.html', {'result': result, 'prompt': prompt})
        elif content_type == 2:

            result = generatesocialmediacaptions(prompt)
            request.session['result'] = result
            # request.session['result'] = result
            # request.session['content_type'] = content_type
            # request.session['prompt'] = prompt
            return render(request, 'result.html', {'result': result, 'prompt': prompt})
        elif content_type == 3:
            result = generateshortstory(prompt)
            return render(request, 'result.html', {'result': result, 'prompt': prompt})
        elif content_type == 4:
            result = generatepoems(prompt)
            request.session['result'] = result
            return render(request, 'result.html', {'result': result, 'prompt': prompt})

    else:

        return render(request, 'result.html',ctx )


# def result(request):
#     if request.method == 'POST':
#         prompt=request.POST['describe']
#         content_type=request.POST['content_type']
#         content_type=int(content_type)
#         if content_type==1:
#             result=generatearticle(prompt)
#             return render(request, 'result2.html',{'result':result,'prompt':prompt})
#         elif content_type==2:
#             result=generatesocialmediacaptions(prompt)
#             return render(request, 'result2.html',{'result':result,'prompt':prompt})
#         elif content_type==3:
#             result=generateshortstory(prompt)
#             return render(request, 'result2.html',{'result':result,'prompt':prompt})
#         elif content_type==4:
#             result=generatepoems(prompt)
#             return render(request, 'result2.html',{'result':result,'prompt':prompt})

#     else:
#        return render(request, 'result2.html', )

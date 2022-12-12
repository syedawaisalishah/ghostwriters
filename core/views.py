from django.conf import settings
import stripe
from django.shortcuts import render, reverse, redirect
import os
import openai
from django.core.cache import cache


openai.api_key = ''
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


def home(request):
    global result
    global content_type
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
        cache.set('content_type', content_type, 120)
        cache.set('prompt', prompt, 120)
        if content_type == 1:
            result = generatearticle(prompt)
            # print(result)
            cache.set('result', result ,120)

        
            return redirect('result')
        elif content_type == 2:

            result = generatesocialmediacaptions(prompt)

            cache.set('result', result, 120)
            
            return render(request, 'result.html')
        elif content_type == 3:
            result = generateshortstory(prompt)
            cache.set('result', result, 120)

            return render(request, 'result.html')
        elif content_type == 4:
            result = generatepoems(prompt)
            cache.set('result', result, 120)

            return render(request, 'result.html')

    else:
        print(session)
        return render(request, 'home.html', {'session_id': session.id, 'stripe_public_key': settings.STRIPE_PUBLIC_KEY, 'amount':session.amount_total//100})


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

   
    contxt={'result':cache.get('result'),'content_type':cache.get('content_type'),'prompt':cache.get('prompt'),
    'session_id':session.id,
    'stripe_public_key':settings.STRIPE_PUBLIC_KEY,
    'amount':session.amount_total//100
    }

    if request.method == 'POST':
        prompt = request.POST['describe']
        content_type = request.POST.get('content_type')
        content_type = int(content_type)
        cache.set('content_type', content_type, 120)
        cache.set('prompt', prompt, 120)
    
        if content_type == 1:
            result = generatearticle(prompt)
            cache.set('result', result ,120)
            return redirect('result')
        elif content_type == 2:
            result = generatesocialmediacaptions(prompt)
            cache.set('result', result, 120)
            return redirect('result')
            # return render(request,'result.html')
        elif content_type == 3:
            result = generateshortstory(prompt)
            cache.set('result', result, 120)
            return redirect('result')
        elif content_type == 4:
            result = generatepoems(prompt)
            cache.set('result', result, 120)
            return redirect('result')

    else:
        # print(contxt)
        return render(request, 'result.html',contxt )




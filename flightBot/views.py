from .models import Bot
from .models import Dialog

from django.conf import settings
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseForbidden
from django.core.exceptions import ObjectDoesNotExist
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.utils.text import Truncator

from linebot import LineBotApi, WebhookParser
from linebot.exceptions import InvalidSignatureError, LineBotApiError
from linebot.models import MessageEvent, TextSendMessage

################
# 這邊自己存好啊 #
################

line_bot_api = LineBotApi(settings.LINE_CHANNEL_ACCESS_TOKEN)
parser = WebhookParser(settings.LINE_CHANNEL_SECRET)

@csrf_exempt

def dialogs(request):
  if request.method == 'GET':
    dialogs = []
    for dialog in Dialog.objects.all():
      dialogs.append({
        'user_name': Truncator(Bot.objects.get(pk=dialog.bot_id).source_id).chars(15) + '...',
        'content': dialog.content,
        'source': dialog.source,
        'created_at': dialog.created_at,
      })
    return render(request, 'dialogs.html', {'dialogs': dialogs})
  else:
    return HttpResponseBadRequest()

def callback(request):
  if request.method == 'POST':
    signature = request.META['HTTP_X_LINE_SIGNATURE']
    body = request.body.decode('utf-8')

    try:
      events = parser.parse(body, signature)
    except InvalidSignatureError:
      return HttpResponseForbidden()
    except LineBotApiError:
      return HttpResponseBadRequest()
    for event in events:
      if event.source.type == 'user':
        try:
          bot = Bot.objects.get(
            source_type = 'user', 
            source_id = event.source.sender_id
          )
        except ObjectDoesNotExist:
          bot = Bot.objects.create(
            source_type = 'user', 
            source_id = event.source.sender_id, 
            status = 1
          )
      if isinstance(event, MessageEvent):
        if event.message.type == 'text':
          Dialog.objects.create(
            bot_id = bot.id,
            content = event.message.text ,
            message_id = event.message.id,              
            source = 'Line'
          )
          line_bot_api.reply_message(
            event.reply_token,
            TextSendMessage(text='收到了，讓我找找～')
          )
    return HttpResponse()
  else:
    return HttpResponseBadRequest()


# 使用者設定條件：
# 航線：TPE<>TYO, TPE<>NRT, TPE<>HNO
# 票種：RT
# 時間：使用者選擇月份，例如：Nov, Dec, Jan, Feb, Mar
# 價格：使用者自由定上限
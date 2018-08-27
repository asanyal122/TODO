import asyncio
import json
from channels.consumer import AsyncConsumer
from channels.db import database_sync_to_async

from .models import Thread,Group,Profile,Todo


class TodoConsumer(AsyncConsumer):
    async def websocket_connect(self,event):
        print ("connected",event)
        me=self.scope['user']
        grps=Profile.objects.get(user=me).group_set.all()
        print (grps)
        for g in grps:
            thread_obj=await self.get_thread(g)
            chat_room="thread_"+thread_obj.group.gid
            await self.channel_layer.group_add(
                chat_room,
                self.channel_name
            )
        self.scope['session']['channel_name']=self.channel_name
        self.scope['session'].save()
        
        try:
            grpid=self.scope['url_route']['kwargs']['grp_id']
            grp=Group.objects.get(id=grpid)
            me=self.scope['user']
            print (me,grp.gname)
            thread_obj=await self.get_thread(grp)
            print (thread_obj.group.gid)
            chat_room="thread_"+thread_obj.group.gid
            #print (chat_room)
            self.chat_room=chat_room
            #print (self.chat_room)
            await self.channel_layer.group_add(
                chat_room,
                self.channel_name
            )
        except:
            pass
        await self.send({
            "type":"websocket.accept"
        })
        #await asyncio.sleep(10)
        
    async def websocket_receive(self,event):
        print ("receive",event)
        front_text=event.get('text',None)
        if front_text is not None:
            loaded_dict_data=json.loads(front_text)
            msg=loaded_dict_data.get('message')
            print (msg)

            grpid=self.scope['url_route']['kwargs']['grp_id']
            grp=Group.objects.get(id=grpid)
            #me=self.scope['user']
            #print (me,grp.gname)
            thread_obj=await self.get_thread(grp)
            print (thread_obj.group.gid)
            chat_room="thread_"+thread_obj.group.gid


            user=self.scope['user']
            username='default'
            if user.is_authenticated:
                username=user.username
            myresponse={
                'message':msg,
                'username':username,
                'group':grp.gname,
            }
            await self.channel_layer.group_send(
                chat_room,
                {
                    "type":"chat_message",
                    "text" : json.dumps(myresponse)
                }
            )

        #     await self.send({
        #     "type" : "websocket.send",
        #     "text" : json.dumps(myresponse)
        # })
    async def chat_message(self,event):
        #print ('message',event)
        await self.send({
            "type":"websocket.send",
            "text":event['text']
        })
    async def websocket_disconnect(self,event):
        print ("disconnected",event)
    
    @database_sync_to_async
    def get_thread(self,group):
        return Thread.objects.get_or_new(group)
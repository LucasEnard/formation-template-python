# 1
# from grongier.pex import BusinessOperation

# class MyBo(BusinessOperation):
#     def on_message(self, request):
#         self.log_info("Hello World")
# 2        
# from hello_world.msg import MyMsg
# from grongier.pex import BusinessOperation

# class MyBo(BusinessOperation):
#     def on_message(self, request):
#         self.log_info("Hello World")
#         response = MyMsg()
#         response.value = "Hello World"
#         return response
# 3
from hello_world.msg import MyMsg
from grongier.pex import BusinessOperation

class MyBo(BusinessOperation):
    def on_message(self, request):
        self.log_info("Hello World")
        response = MyMsg()
        response.value = "Hello World"
        return response

    def on_my_msg(self, request: MyMsg):
        self.log_info("Hello World")
        response = MyMsg()
        response.value = f"Hello World {request.value}"
        return response


class APIErrorResponse:

    def __init__(self,status,error):
        self.status=status
        self.error=error
    
    def respond(self):
        return({
            "status":self.status,
            "error":self.error
        })
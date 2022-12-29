import datetime

class UserSession:
    def __init__(self, session_collection):
        self.session_objects = {}
        self.session_collection = session_collection
        for user_session in self.session_collection.find({}):
            self.session_objects[str(user_session["_id"])] = {
                "email":user_session["email"],
                "person_id":user_session["person_id"],
                "display_name":user_session["display_name"],
                "avatar":user_session["avatar"]
                }

        
        
    def isUserSessionActive(self,user_session_id):
        user_session_obj = self.session_objects.get(user_session_id)
        if user_session_obj == None:
            return False,{}
            
        return True, user_session_obj
        
        
    def addUserToSession(self, access_token, person_id, email, display_name, avatar_url):
        try:
            self.session_collection.delete_many({"person_id":person_id})
            
            user_session_id = self.session_collection.insert_one({
                "access_token":access_token,
                "person_id":person_id,
                "email":email,
                "display_name":display_name,
                "avatar":avatar_url,
                "created_at":datetime.datetime.now()
            }).inserted_id
            self.session_objects = {}
            for user_session in self.session_collection.find({}):
                self.session_objects[str(user_session["_id"])] = {
                    "email":user_session["email"],
                    "person_id":user_session["person_id"],
                    "display_name":user_session["display_name"],
                    "avatar":user_session["avatar"]
                    }
                
            return True, str(user_session_id)
        except Exception as e:
            print(e)
            return False,""
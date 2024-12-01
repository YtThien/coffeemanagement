class Staff:
    def __init__(self,id,name_staff,phone,email,position,username,password,id_role):
        self.id = id
        self.name_staff = name_staff
        self.phone = phone
        self.email = email
        self.position = position
        self.username =  username
        self.password = password
        self.id_role = id_role
    def __repr__(self):
        return f"Staff({self.id},{self.name},{self.phone},{self.email},{self.position},{self.username},{self.password},{self.id_role})"
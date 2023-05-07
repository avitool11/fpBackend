from flask import Flask,request,jsonify
from flask_restful import Resource, Api, reqparse
import handlers as handler
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

api = Api(app)


@app.route("/",methods=['GET'])
def healthCheck():
    return jsonify({"result":"Hello World"})

@app.route('/registration',methods = ['POST'])
def registration(): #Done
    if request.method == 'POST':
        print("Incoming Request")
        name = request.json['name']
        email = request.json['email']
        password = request.json['password']
        role = request.json['role']
        dob = request.json['dob']
        return jsonify({"result":handler.registrationHandler(name,email,password,role,dob)})

@app.route('/login',methods = ['POST'])
def login(): #Done
    email = request.json['email']     
    password = request.json['password']
    return jsonify({"result":handler.loginHandler(email,password)})

@app.route('/approval',methods = ['POST','GET'])
def approvalAdmin(): #Done
    if request.method == 'POST':
        userId = request.json['user_id']
        adminId = request.json ['admin_id']
        return jsonify({"result":handler.approvalHandler(userId,adminId)})
    if request.method == 'GET':
        adminId = request.args.get('user_id')
        return jsonify({"result":handler.getDueApprovals(adminId)}) 
@app.route('/editProfile', methods = ['POST'])
def editProfile(): #Done
    userId = request.json['user_id']
    passwordOld = request.json['old_password']
    passwordNew = request.json['new_password']
    return jsonify({"result":handler.editProfile(userId,passwordOld,passwordNew)})

@app.route('/assignment', methods =['GET','POST'])
def assignAssignment(): #Done
    if request.method == 'POST':
        userId = request.json['user_id']
        questions = request.json['questions']
        batchId = request.json['batch']
        courseId = request.json['course']
        return jsonify({"result":handler.assignAssignment(userId, questions, batchId, courseId)})
    if request.method == 'GET':
        userId = request.args.get('user_id')
        # print(userId)
        return jsonify({"result":handler.getFacultyBatchCourseDetails(userId)})

@app.route('/viewAssignment', methods=['GET'])
def viewAssignment(): #Done
    userId = request.args.get('user_id')
    return jsonify({"result":handler.viewAssignment(userId)})

@app.route('/viewTimetable', methods=['GET'])
def viewTimetable(): #Done
    userId = request.json['user_id']
    return jsonify({"result":handler.viewTimetable(userId)})

@app.route('/uploadTimetable', methods=['POST'])
def uploadTimetable(): #Done
    userId = request.json['user_id']
    data = request.json['data']
    # courseId = request.json['course_id']
    batchId = request.json['batch_id']
    return jsonify({"result":handler.uploadTimetable(userId,data,batchId)})

@app.route('/feedback', methods =['POST','GET'])
def uploadFeedback(): #Done
    if request.method == 'POST':
        userId = request.json['user_id']
        courseId = request.json['course_id']
        feedback = request.json ['feedback']
        return jsonify({"result":handler.uploadFeedback(userId,courseId,feedback)})
    if request.method == 'GET':
        userId = request.args.get('user_id')         
        return jsonify({"result":handler.getStudentBatchCourseDetails(userId)}) 

@app.route('/uploadInternalResult', methods = ['POST','GET'])
def uploadInternalResult(): #Done
    if request.method == 'POST':
        userId = request.json['user_id']
        data = request.json['data']
        batchId = request.json['batch_id']
        courseId = request.json['course_id']
        return jsonify({"result":handler.uploadInternalResult(userId,data,batchId,courseId)}) 
    if request.method == 'GET':
        userId = request.args.get('user_id')         
        return jsonify({"result":handler.getFacultyBatchCourseDetails(userId)})

@app.route('/uploadExternalResult', methods = ['POST', 'GET'])
def uploadExternalResult(): #Done
    if request.method == 'POST':
        userId = request.json['user_id']
        data = request.json['data']
        batchId = request.json['batch_id']
        courseId = request.json['course_id']
        return jsonify({"result":handler.uploadExternalResult(userId,data,batchId,courseId)})
    if request.method == 'GET':
        return jsonify({"result":handler.getAllBatchCourseDetails()}) 

@app.route('/notice', methods = ['POST','GET'])
def uploadNotice(): #Done
    if request.method == 'POST':
        userId = request.json['user_id']
        batchId = request.json['batch_id']
        courseId = request.json['course_id']
        noticeData = request.json['notice_data']
        return jsonify({"result":handler.uploadNotice(userId,batchId,courseId,noticeData)})
    if request.method == 'GET':
        userId = request.args.get('user_id')       
        return jsonify({"result":handler.getFacultyBatchCourseDetails(userId)})

@app.route('/viewNotice',methods = ['POST','GET'])
def viewNotice(): #Done
    if request.methods == 'POST':
        batchId = request.json['batch_id']
        courseId = request.json['course_id']
        return jsonify({"result":handler.viewNotice(batchId,courseId)})
    if request.methods == 'GET':
        return jsonify({"result":handler.getAllBatchCourseDetails()}) 

@app.route('/uploadAttendance',methods=['POST','GET'])
def attendanceDetails(): #Done
    if request.methods == 'POST':
        userId = request.json['user_id']
        batchId = request.json['batch_id']
        courseId = request.json['course_id']
        date = request.json['date']
        students_list = request.json['students_list']
        attendace_list = request.json['attendance_list']
        return jsonify({"result":handler.uploadAttendance(userId,batchId,courseId,date,students_list,attendace_list)})

    if request.methods == 'GET':
        userId = request.args.get('user_id')
        return jsonify({"result":handler.getFacultyBatchCourseDetails()}) 

@app.route('/viewResult',methods = ['POST'])
def resultDetails(): #Done
    if request.methods == 'POST':
        userId = request.json['user_id']
        return jsonify({"result":handler.getResult(userId)}) 

@app.route('/viewAttendance', methods = ['POST','GET'])
def viewAttendance(): #Done
    if request.methods == 'POST':
        userId = request.json['user_id']
        courseId = request.json['course_id']
        return jsonify({"result":handler.viewAttendance(userId,courseId)})
    if request.methods == 'GET':
        userId = request.args.get('user_id')
        return jsonify({"result":handler.getStudentBatchCourseDetails(userId)}) 

@app.route('/editStudentDetails', methods = ['POST','GET','DELETE'])
def updateStudentDetails(): #Done
    if request.methods == 'POST':
        userId = request.json['user_id']
        studentId = request.json['student_id']
        email = request.json['new_email']
        dob = request.json['dob']
        name = request.json['name']
        return jsonify({"result":handler.updateStudentDetails(userId,studentId,email,dob,name)}) #This POST request will Update the student details
    if request.methods == 'GET':
        userId = request.args.get('user_id')
        return jsonify({"result":handler.getFacultyStudents(userId)}) #A Faculty can change Student Details. This GET request will fetch all the students under the faculty
    if request.methods == 'PUT': 
        userId = request.json['user_id']
        studentId = request.json['student_id']
        return jsonify({"result":handler.deleteStudent(userId,studentId)}) #This Delete request will delete the user})

@app.route('/addCourse')
def addCourse(): #Done
    if request.methods == 'POST':
        userId = request.json['user_id']
        courseName = request.json['course_name']
        courseCode = request.json['course_code']
        return jsonify({"result":handler.addNewCourse(userId,courseCode,courseName)}) 
    
@app.route('/assignCourse', methods = ['POST','GET'])
def assignCourse(): #Done
    if request.methods == 'POST':
        userId = request.json['user_id']
        courseCode = request.json['course_code']
        facultyId = request.json['faculty_id']
        return jsonify({"result":handler.assignCourse(userId,courseCode,facultyId)})
    if request.methods == 'GET':
        userId = request.json['user_id']
        return jsonify({"result":handler.getAllCourses(userId)})

if __name__ == '__main__':
    app.run()

# Udacity tool to submit and download programming quizzes
# by: Karl-Aksel Puulmann, macobo@ut.ee

import cookielib
import urllib
import urllib2
import json
import re
from itertools import ifilter
import getpass
import os
import time

rootURL = r"http://www.udacity.com"
ajaxRoot = r"http://www.udacity.com/ajax"

coursePath = {
    # Intro to Computer Science. Building a Search Engine
    101: r"Course/cs101/CourseRev/apr2012",
    # Web Application Engineering. How to Build a Blog
    253: r"Course/cs253/CourseRev/apr2012",
    # Programming Languages. Building a Web Browser
    262: r'Course/cs262/CourseRev/apr2012',
    # Artificial Intelligence. Programming a Robotic Car
    373: r"Course/cs373/CourseRev/apr2012",
    # Design of Computer Programs. Programming Principles
    212: r"Course/cs212/CourseRev/apr2012",
    # Algorithms. Crunching Social Networks
    215: r"Course/cs215/CourseRev/1",
    # Applied Cryptography. Science of Secrets
    387: r"Course/cs387/CourseRev/apr2012",
    # Software Testing. How to Make Software Fail
    258: r"Course/cs258/CourseRev/1"
}

courseCache = {}
csrf_token = None
uVersion = None
logged_in = False

def log_in():
    """ Logs you in so you can submit a problem """
    global logged_in
    email = raw_input("Email: ")
    # Try to ask for password in a way that shoulder-surfers can't handle
    pw = getpass.getpass("Password: ")
    data = {"data":
                {"email":email,
                 "password":pw},
            "method":"account.sign_in",
            "version":uVersion,
            "csrf_token":csrf_token}
    try:
        answer = jsonFromURL(ajaxRoot, json.dumps(data))
    except urllib2.HTTPError, error:
        contents = error.read()
        print(contents)
        raise
    if 'error' in answer['payload']:
        raise ValueError("Failed to log in!")
    print("Logged in successfully!")
    logged_in = True
        
def setSessionHandler():
    """ Gets information from udacity home page to successfully query courses """
    global uVersion, csrf_token
    cj = cookielib.CookieJar()
    opener = urllib2.build_opener(urllib2.HTTPCookieProcessor(cj))
    urllib2.install_opener(opener)
    uMainSiteHTML = urllib2.urlopen(rootURL).read()
    # get uVersion - used when querying
    uVersion = re.findall(r"js/udacity.js[?]([0-9]+)", uMainSiteHTML)[0]
    uVersion = "dacity-"+uVersion
    # get csrf_token - used for logging in
    csrf_token = re.findall(r'csrf_token = "([^"]+)', uMainSiteHTML)[0]

def sanitize(path):
    """ Sanitizes unit names """
    illegalChars = r'<>:"/\|?*'
    for ch in illegalChars:
        path = path.replace(ch, "")
    return path

# -- Utility functions --
def jsonFromURL(url, data=None):
    return json.loads(urllib2.urlopen(url, data).read())

def findPair(key, value, json_array):
    """ Finds first dictionary that where key corresponds to value
        in an array of dictionaries """
    for x in json_array:
        if x is not None and key in x and x[key] == value:
            return x
    raise ValueError("(key, value) pair not in list")

def ajaxURL(query):
    return ajaxRoot + "?" + urllib.quote(json.dumps(query))

# -- Functions related to getting course-related info --
def courseJSON(courseID):
    """ Returns the JSON-formatted info about this course """
    if courseID not in courseCache:
        query = {"data":{"path":coursePath[courseID]},
                 "method": "course.get",
                 "version": uVersion}
        print("Getting course info...")
        url = ajaxURL(query)
        courseCache[courseID] = jsonFromURL(url)['payload']
    return courseCache[courseID]
        

def unitJSON(courseID, unitName):
    """ Returns the JSON of this unit from the API """
    courseJS = courseJSON(courseID)
    
    unitJS = next(x for x in courseJS['course_rev']['units'] \
                  if x['name'] == unitName)
    return unitJS

def programPath(unitJSON, n):
    """ Given the JSON covering the unit, returns the nth part programming quiz path """
    partKeys = unitJSON['nuggetLayout'][n-1] # The keys to parts of part n
    nuggets = unitJSON['nuggets']
    for v in partKeys: # one of the parts should be a programming quiz
        if v is not None:
            part = findPair('key', v['nugget_key'], nuggets)
            type_of_lecture = part['nuggetType']
            if type_of_lecture == "program":
                return part['path']
    raise ValueError("Found no programming quiz for this part")

def programmingQuiz(courseID, unit, part):
    """ Returns the program text for Udacity cs-courseID unit part quiz """
    print("Getting default program text...")
    path = programPath(unitJSON(courseID, unit), part)
    query = {"data":{"path": path},
             "method":"assignment.ide.get",
             "version": uVersion}
    url = ajaxURL(query)
    queryAnswer = jsonFromURL(url)
    return queryAnswer['payload']['nugget']['suppliedCode']


def downloadProgram(courseID, unit, part):  
    """ Downloads the specific program and places it as
        ./courseID/Unit/part.py in the file tree
        (./ means current folder)
        Places a token on the first line to identify the file. """
    text = programmingQuiz(courseID, unit, part)
    coursePath = os.path.join(os.curdir, str(courseID))
    if not os.path.exists(coursePath):
        os.mkdir(coursePath)

    unit = sanitize(unit)
    unitPath = os.path.join(coursePath, unit)
        
    if not os.path.exists(unitPath):
        os.mkdir(unitPath)
    fileName = "{0}.py".format(part)
    filePath = os.path.join(unitPath, fileName)
    if os.path.exists(filePath):
        raise ValueError("File already exists")
    with open(filePath, "w") as out:
        # Add info to help identify file
        out.write("# {0} ; {1} ; {2}\n".format(courseID, unit, part))
        out.write('\n'.join(text.split("\r\n")))

def downloadUnit(courseID, unit):
    unitJS = unitJSON(courseID, unit)
    parts = len(unitJS['nuggetLayout'])
    for part in range(1, parts+1):
        print('{0}: {1} part {2}'.format(courseID, unit, part))
        try:
            downloadProgram(courseID, unit, part)
        except ValueError:
            pass

def downloadCourse(courseID):
    """ Downloads all units in this course """
    courseJS = courseJSON(courseID)
    for unit in courseJS['course_rev']['units']:
        unitName = unit['name']
        print('{0}: {1}'.format(courseID, unitName))
        downloadUnit(courseID, unitName)


# -- Functions related to submitting a file --
def identifyFile(first_line):
    """ Tries to identify file by its first line, which must
        be in the following form: "# CourseID ; Unit ; Part" """
    if first_line[:2] != '# ':
        raise ValueError("First line doesn't identify file")
    try:
        course, unit, part = first_line[2:].strip().split(' ; ')
    except:
        raise ValueError("First line doesn't identify file")
    return int(course), unit, int(part)

def submit(program_file):
    """ Submits a file, trying to identify it by its first line """
    with open(program_file) as f:
        first_line = f.readline() # identifier line
        program_text = f.read()
    course, unit, part = identifyFile(first_line)
    status = submitSolution(program_text, course, unit, part)

def submitSolution(program_text, courseID, unit, part):
    global logged_in
    if not logged_in:
        log_in()
    path = programPath(unitJSON(courseID, unit), part)
    # Send the program as a query
    print("Submitting your solution for CS{0} {1} Part {2}".format(courseID, unit, part))
    query = {"data":{"usercode":program_text,
                     "op":"submit",
                     "path":path},
             "method":"assignment.ide.exe",
             "version":uVersion,
             "csrf_token":csrf_token}
    req = urllib2.Request(ajaxRoot, json.dumps(query))
    response1 = json.loads(urllib2.urlopen(req).read())
    # Ask from the server how we did
    query = {"data": {"ps_key": response1['payload']['ps_key']},
             "method":"assignment.ide.result",
             "version":uVersion}
    queryURL = ajaxURL(query)
    for _ in range(20):
        specifics = jsonFromURL(queryURL)
        if specifics['payload']['status'] != 'queued':
            print("\nThe server responded:")
            print(specifics['payload']['comment'])
            return specifics['payload']
        print("Your program is still being graded. Trying again in 1 second")
        time.sleep(1)
    print("Your program didn't recieve a response in 20 tries. :(")

def main():
    import argparse

    epilog = """Example:\n\tpquiz.py --submit -c 262 -u "Unit 5" -p 11
\tpquiz.py --download --course 212"""
    parser = argparse.ArgumentParser(description= \
                "Tool to help download and upload programming quizzes from Udacity's CS courses", 
                epilog = epilog,
                formatter_class = argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-s", "--submit",
                        action='store_true',
                        help="submit a file")
    parser.add_argument("-d", "--download",
                        action='store_true',
                        help="download a programming quiz")
    parser.add_argument("-c", "--course",
                        type=int,
                        metavar="CID",
                        help="Course ID (csCID)")
    parser.add_argument("-u", "--unit",
                        help='Unit title (eg "Unit 5", "Homework 2")')
    parser.add_argument("-p", "--part",
                        type=int,
                        help="part number")
    parser.add_argument("-f", "--file",
                        help="path to file")
    
    args = parser.parse_args()
    
    if args.submit and not args.download:
        setSessionHandler()
        if args.course and args.unit and args.part and args.file:
            program_text = open(args.file).read()
            submitSolution(program_text, args.course, args.unit, args.part)
        elif args.file:
            submit(args.file)
        else:
            parser.print_help()
    elif args.download and not args.submit:
        setSessionHandler()
        if args.course and args.unit and args.part:
            downloadProgram(args.course, args.unit, args.part)
        elif args.course and args.unit:
            downloadUnit(args.course, args.unit)
        elif args.course:
            downloadCourse(args.course)
        else:
            parser.print_help()
    else:
        parser.print_help()

if __name__ == "__main__":
    main()

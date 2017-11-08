#! /usr/bin/python

import cgi
import cgitb
cgitb.enable()

from operator import itemgetter

header='Content-type: text/html\n\n'

bad_login='<p style="color:red;" align="center">ERROR: Passwords do not match.</p>'
bad_login2='<p style="color:red;" align="center">ERROR: Username taken.</p>'
bad_login3='<p style="color:red;" align="center">ERROR: Incorrect password.</p>'
bad_login4='<p style="color:red;" align="center">ERROR: Username not found.</p>'
image='https://cdn2.iconfinder.com/data/icons/flat-avatars-1/512/Percy-512.png'

js_table_top='''
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
      google.charts.load('current', {'packages':['table']});
      google.charts.setOnLoadCallback(drawTable);

      function drawTable() {
        var data = new google.visualization.DataTable();
        data.addColumn('string', 'Date');
        data.addColumn('string', 'Opponent');
        data.addColumn('string', 'Points');
        data.addColumn('string', 'Assists');
        data.addColumn('string', 'Rebounds');
        data.addColumn('string', 'Turnovers');
        data.addRows([
        '''

          #['Mike',  {v: 10000, f: '$10,000'}, true],
          #['Jim',   {v:8000,   f: '$8,000'},  false],
          #['Alice', {v: 12500, f: '$12,500'}, true],
          #['Bob',   {v: 7000,  f: '$7,000'},  true]

js_table_bottom='''
        ]);
        var table = new google.visualization.Table(document.getElementById('table_div'));

        table.draw(data, {width: '100%', height: '100%'});
      }
    </script>
'''

js_graph_top='''
    <script type="text/javascript" src="https://www.gstatic.com/charts/loader.js"></script>
    <script type="text/javascript">
        google.charts.load('current', {packages: ['corechart', 'line']});
        google.charts.setOnLoadCallback(drawCurveTypes);

        function drawCurveTypes() {
              var data = new google.visualization.DataTable();
              data.addColumn('date', 'X');
              data.addColumn('number', 'Points');
              data.addColumn('number', 'Assists');
              data.addColumn('number', 'Rebounds');
              data.addColumn('number', 'Turnovers');

              data.addRows([
              
              '''

js_graph_bottom='''
          ]);

          var options = {
            hAxis: {
              title: 'Date'
            },
            vAxis: {
              title: 'Frequency'
            },
          };

          var chart = new google.visualization.LineChart(document.getElementById('table_div'));
          chart.draw(data, options);
        }
    </script>
'''

def enter():
    form=cgi.FieldStorage()
 
    if "submit_signup" in form:
        firstname=form.getvalue('firstname')
        lastname=form.getvalue('lastname')
        username=form.getvalue('username')
        password=form.getvalue('password')
        password2=form.getvalue('confirmpwd')
        if password != password2:
            print header
            return updateFile('signup.html','<!--bad_login-->',bad_login)
        else:
            user_data=convert_to_list()
            for a in user_data:
                if a[0]==username:
                    print header
                    return updateFile('signup.html','<!--bad_login-->',bad_login2)
            wr=open(username+'.txt','w')
            wr.write('')
            wr.close()
            lst=[username,firstname,lastname,password,image]
            user_data.append(lst)
            convert_to_text(user_data)
            profile=readFile('profile.html')
            profile=profile.replace('!NAME',firstname.upper())
            profile=profile.replace('!username',username)
            profile=profile.replace('!P','N/A')
            profile=profile.replace('!A','N/A')
            profile=profile.replace('!R','N/A')
            print header
            print profile
            return

    if "submit_login" in form:
        username=form.getvalue('username')
        password=form.getvalue('password')
        user_data=convert_to_list()
        for a in user_data:
            if a[0]==username:
                if a[3]==password:
                    personal_data=convert_to_list2(username+'.txt')
                    if readFile(username+'.txt')=='':
                        profile=readFile('profile.html')
                        profile=profile.replace('!NAME',a[1].upper())
                        profile=profile.replace('!username',username)
                        profile=profile.replace(image,a[4])
                        profile=profile.replace('!P','N/A')
                        profile=profile.replace('!A','N/A')
                        profile=profile.replace('!R','N/A')
                        print header
                        print profile
                        return
                    total_points=0
                    total_assists=0
                    total_rebounds=0
                    for b in personal_data:
                        total_points+=int(b[2])
                        total_assists+=int(b[3])
                        total_rebounds+=int(b[4])
                    total_points=round(float(total_points)/len(personal_data),1)
                    total_assists=round(float(total_assists)/len(personal_data),1)
                    total_rebounds=round(float(total_rebounds)/len(personal_data),1)
                    profile=readFile('profile.html')
                    profile=profile.replace('!NAME',a[1].upper())
                    profile=profile.replace('!username',a[0])
                    profile=profile.replace(image,a[4])
                    profile=profile.replace('!P',str(total_points))
                    profile=profile.replace('!A',str(total_assists))
                    profile=profile.replace('!R',str(total_rebounds))
                    print header
                    print profile
                    return
                    #s=updateFile('profile.html','!NAME',a[1].upper())
                    #t=updateFile(s,'!username',a[0])
                    #return updateFile(t,image,a[4])
                else:
                    print header
                    return updateFile('login.html','<!--bad_login-->',bad_login3)
        print header
        return updateFile('login.html','<!--bad_login-->',bad_login4)

    if "submit_addgame" in form:
        username=form.getvalue('hidden_username')
        date=form.getvalue('date')
        opponent=form.getvalue('opponent')
        points=str(form.getvalue('points'))
        assists=str(form.getvalue('assists'))
        rebounds=str(form.getvalue('rebounds'))
        turnovers=str(form.getvalue('turnovers'))
        lst=[date,opponent,points,assists,rebounds,turnovers]
        personal_data=convert_to_list2(username+'.txt')
        personal_data.append(lst)
        convert_to_text2(personal_data,username+'.txt')
        addgame=readFile('addgame.html')
        addgame=addgame.replace('<p>All fields are required.</p>','<p>All fields are required | Your game has been added to your <b>STATISTICS</b>.</p>')
        addgame=addgame.replace('!username',username)
        print header
        print addgame
        return

    if "submit_image" in form:
        username=form.getvalue('hidden_username')
        image_url=form.getvalue('image_url')
        user_data=convert_to_list()
        for a in user_data:
            if a[0]==username:
                a[4]=image_url
                convert_to_text(user_data)
                personal_data=convert_to_list2(username+'.txt')
                if readFile(username+'.txt')=='':
                    profile=readFile('profile.html')
                    profile=profile.replace('!NAME',a[1].upper())
                    profile=profile.replace('!username',username)
                    profile=profile.replace(image,a[4])
                    profile=profile.replace('!P','N/A')
                    profile=profile.replace('!A','N/A')
                    profile=profile.replace('!R','N/A')
                    print header
                    print profile
                    return
                total_points=0
                total_assists=0
                total_rebounds=0
                for b in personal_data:
                    total_points+=int(b[2])
                    total_assists+=int(b[3])
                    total_rebounds+=int(b[4])
                total_points=round(float(total_points)/len(personal_data),1)
                total_assists=round(float(total_assists)/len(personal_data),1)
                total_rebounds=round(float(total_rebounds)/len(personal_data),1)
                profile=readFile('profile.html')
                profile=profile.replace('!NAME',a[1].upper())
                profile=profile.replace('!username',a[0])
                profile=profile.replace(image,a[4])
                profile=profile.replace('!P',str(total_points))
                profile=profile.replace('!A',str(total_assists))
                profile=profile.replace('!R',str(total_rebounds))
                print header
                print profile
                return
    
    if "button_profile" in form:
        username=form.getvalue('hidden_username')
        user_data=convert_to_list()
        for a in user_data:
            if a[0]==username:
                personal_data=convert_to_list2(username+'.txt')
                if readFile(username+'.txt')=='':
                    profile=readFile('profile.html')
                    profile=profile.replace('!NAME',a[1].upper())
                    profile=profile.replace('!username',username)
                    profile=profile.replace(image,a[4])
                    profile=profile.replace('!P','N/A')
                    profile=profile.replace('!A','N/A')
                    profile=profile.replace('!R','N/A')
                    print header
                    print profile
                    return
                total_points=0
                total_assists=0
                total_rebounds=0
                for b in personal_data:
                    total_points+=int(b[2])
                    total_assists+=int(b[3])
                    total_rebounds+=int(b[4])
                total_points=round(float(total_points)/len(personal_data),1)
                total_assists=round(float(total_assists)/len(personal_data),1)
                total_rebounds=round(float(total_rebounds)/len(personal_data),1)
                profile=readFile('profile.html')
                profile=profile.replace('!NAME',a[1].upper())
                profile=profile.replace('!username',a[0])
                profile=profile.replace(image,a[4])
                profile=profile.replace('!P',str(total_points))
                profile=profile.replace('!A',str(total_assists))
                profile=profile.replace('!R',str(total_rebounds))
                print header
                print profile
                return
    
    if "button_addgame" in form:
        username=form.getvalue('hidden_username')
        print header
        return updateFile('addgame.html','!username',username)
    
    if "submit_graph" in form:
        username=form.getvalue('hidden_username')
        personal_data=convert_to_list2(username+'.txt')
        if readFile(username+'.txt')=='':
            statistics=readFile('statistics.html')
            statistics=statistics.replace('!username',username)
            statistics=statistics.replace('<p></p>','<p>No data has been provided yet.</p>')
            print header
            print statistics
            return
        personal_data=sorted(personal_data,key=itemgetter(0))
        #graph
        plot=''
        for a in personal_data:
            datelst=a[0].split('-')
            date='new Date('+datelst[0]+','+str(int(datelst[1])-1)+','+datelst[2]+')'
            lst='['+date+','+a[2]+','+a[3]+','+a[4]+','+a[5]+'],'
            plot+=lst
        graph_script=js_graph_top+plot+js_graph_bottom
        statistics=readFile('statistics.html')
        #statistics=statistics.replace('<p>No data has been provided yet.</p>','')
        statistics=statistics.replace('!username',username)
        statistics=statistics.replace('<!--js-->',graph_script)
        #statistics=statistics.replace('<!--js2-->',graph_script)
        print header
        print statistics
        return

    if "button_statistics" or "submit_table" in form:
        username=form.getvalue('hidden_username')
        personal_data=convert_to_list2(username+'.txt')
        if readFile(username+'.txt')=='':
            statistics=readFile('statistics2.html')
            statistics=statistics.replace('!username',username)
            statistics=statistics.replace('<p></p>','<p>No data has been provided yet.</p>')
            print header
            print statistics
            return
        personal_data=sorted(personal_data,key=itemgetter(0))
        #table
        rows=''
        for a in personal_data:
            rows+=str(a)+','
        table_script=js_table_top+rows+js_table_bottom
        statistics=readFile('statistics2.html')
        #statistics=statistics.replace('<p>No data has been provided yet.</p>','')
        statistics=statistics.replace('!username',username)
        statistics=statistics.replace('<!--js-->',table_script)
        #statistics=statistics.replace('<!--js2-->',graph_script)
        print header
        print statistics
        return
    
def convert_to_list():
    try:
        f=open("directory.txt")
        s=f.read().split('\n') 
        f.close()
        masterlist=[]
        for i in s:
            lst=i.split(',')
            #if len(lst)>=4:
		#newlst=[lst[0],lst[1],lst[2]]
		#for a in range(3,len(lst)):
                    #individ_task=lst[a].split('//')
                    #newlst.append(individ_task)
                #lst=newlst
            masterlist.append(lst)
    except:
        return []
    return masterlist  

def convert_to_text(masterlist):
    lst1=[]
    if masterlist[0]==['']:
        masterlist=masterlist[1:]
    if masterlist[-1]==['']:
        masterlist=masterlist[:-1]
    for a in masterlist:
        #if len(a)>=4:
            #user_info=[a[0],a[1],a[2]]
            #for b in range(3,len(a)): # b is a number (index)
                #individ_task='//'.join(a[b])
                #user_info.append(individ_task)
            #user=','.join(user_info)
            #lst1.append(user)
        #else:
        user=','.join(a)
        lst1.append(user)
    txt='\n'.join(lst1)
    wr=open("directory.txt",'w')
    wr.write(txt)
    return

def convert_to_list2(filename):
    try:
        f=open(filename)
        s=f.read().split('\n') 
        f.close()
        masterlist=[]
        for i in s:
            lst=i.split(',')
            #if len(lst)>=4:
		#newlst=[lst[0],lst[1],lst[2]]
		#for a in range(3,len(lst)):
                    #individ_task=lst[a].split('//')
                    #newlst.append(individ_task)
                #lst=newlst
            masterlist.append(lst)
    except:
        return []
    return masterlist  

def convert_to_text2(masterlist,filename):
    lst1=[]
    if masterlist[0]==['']:
        masterlist=masterlist[1:]
    if masterlist[-1]==['']:
        masterlist=masterlist[:-1]
    for a in masterlist:
        #if len(a)>=4:
            #user_info=[a[0],a[1],a[2]]
            #for b in range(3,len(a)): # b is a number (index)
                #individ_task='//'.join(a[b])
                #user_info.append(individ_task)
            #user=','.join(user_info)
            #lst1.append(user)
        #else:
        user=','.join(a)
        lst1.append(user)
    txt='\n'.join(lst1)
    wr=open(filename,'w')
    wr.write(txt)
    return
    
def readFile(filename):
    try:
        f=open(filename,'rU')
        s=f.read()
        f.close()
    except:
        s=''
    return s

def updateFile(filename,old,new):
    file_string=readFile(filename)
    file_string=file_string.replace(old,new)
    print file_string
    
enter()

import appuifw, e32, location, time, os, httplib, urllib, appswitch, sysinfo, messaging, switchoff, PyKeyLock, thread, audio, globalui, uikludges
from e32db import format_time
from time import *
appuifw.app.screen='normal'
from keypress import simulate_key 
from audio import *
appuifw.app.title=u'CellLocation'
def ru(x):return x.decode('utf-8') 
olaylaretkin=1
txt = appuifw.Text()
appuifw.app.body = txt
appuifw.app.body.color = (0,
 0,
 0) 
yapildi=0 
lockey=0
bosluk=" "

def arkaplan():
    appswitch.switch_to_bg(u"CellLocation")
def kaydet():
    CONFIG_DIR='E:/System/Apps/CellLocation'
    CONFIG_FILE=os.path.join(CONFIG_DIR,'mysettings.txt')
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        CONFIG_FILE=os.path.join(CONFIG_DIR,'mysettings.txt')      
    config={}
    config['variable1']= prgdili
    config['sp']= standartprofile
    config['sure']= sure
    f=open(CONFIG_FILE,'wt')
    f.write(repr(config))
    f.close()
    oku() 
 
def oku():
    CONFIG_FILE='E:/System/Apps/CellLocation/mysettings.txt'
    try:
        f=open(CONFIG_FILE,'rt')
        try:
            content = f.read()
            config=eval(content)
            f.close()
            global prgdili
            prgdili=config.get('variable1','')
            global standartprofile
            standartprofile=config.get('sp','')
            global sure
            sure=config.get('sure','')
        except:
            print 'dosya okunamiyor'
    except:
        print 'dosya acilamiyor'
oku()


try:
   miso.compress_all_heaps()
except:
   pass


class FileSelector:
    def __init__(self,dir=".",ext='.jpg'):
        self.dir = dir
        self.ext = ext
        self.files = {}
 
        def iter(fileselector,dir,files):
            for file in files:
                b,e = os.path.splitext(file)
                if e == fileselector.ext:
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)
 
        os.path.walk(self.dir,iter,self)
        self.sortedkeys = self.files.keys()
        self.sortedkeys.sort()
 
    def GetKeys(self):
        return self.sortedkeys
 
    def GetFile(self,index):
        return self.files[self.sortedkeys[index]]
class MusicSelector:
    def __init__(self,dir=".",ext='.jpg'):
        self.dir = dir
        self.ext = ext
        self.files = {}
 
        def iter(fileselector,dir,files):
            for file in files:
                b,e = os.path.splitext(file)
                if e == ".mp3":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)
                if e == ".aac":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)                 
                if e == ".MP3":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)
                if e == ".AAC":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)  
                if e == ".mid":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)
                if e == ".MID":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)                 
                if e == ".amr":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)
                if e == ".AMR":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)   
                if e == ".wav":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file) 
                if e == ".WAV":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)                                             
        try:     
            os.path.walk(self.dir,iter,self)
        except:
            pass
        self.sortedkeys = self.files.keys()
        self.sortedkeys.sort()
 
    def GetKeys(self):
        return self.sortedkeys
 
    def GetFile(self,index):
        return self.files[self.sortedkeys[index]]


def dilsec():
    appuifw.note(ru("Please select your language"), 'conf')
    selector = FileSelector("e:\\System\\Apps\\CellLocation\\langs",".lang")
    index = appuifw.selection_list(selector.GetKeys())
    if index is not None:
        appuifw.note(u"File %s selected." % selector.GetFile(index), "info")
        global prgdili
        prgdili=selector.GetFile(index)
    else:
        appuifw.note(u"No file selected.", "info")
        global prgdili
        prgdili='0'
    kaydet()    
    dil() 
 

def dil(): 
    oku()
    if prgdili=='0':
        dilsec()
    else:
        try:
            f=file(prgdili,'rb')
            global language
            language=f.read().split('\n')
            f.close()
        except:
            appuifw.note(ru("Language file is damaged."),'error')
            dilsec()        
            
dil()

def lang(string):
    return language[string-1]
uikludges.set_right_softkey_text(ru(lang(105)))    
def hakkinda():
    globalui.global_msg_query(ru("İlkTık CellLocation\nVersion: 2.0\nDeveloped By: Oğuz Kırat\n(c) 2008 İlkTik.com\nhttp://www.ilktik.com/celllocation\nThere is no responsibility for web pages you connected to get map and location information. Location information may be wrong.\n\nİlkTık CellLocation\nSürüm: 2.0\nGeliştiren: Oğuz Kırat\n(c) 2008 İlkTik.com\nhttp://www.ilktik.com/celllocation\nBilgi ve harita almak için bağlandığınız adresler hakkında sorumluluk kabul edilmemektedir. Yer bilgisi her zaman doğru olmayabilir."), ru("About"))


if sysinfo.active_profile()==u"offline":
    appuifw.note(ru(lang(77)))
         
PATH = u"E:\\System\\Apps\\CellLocation\\"  
if not os.path.exists(PATH):  
        os.makedirs(PATH)  
 
INTERVAL = 5.0  
CELL_FILE = PATH + "known_cells.txt" 
CLDB_FILE = PATH + "icldb.ilktik"  
SCELLS_FILE = PATH + "scells.ilktik" 

LOG_FILE = PATH + "visited_cells.txt"  
log = file(LOG_FILE, "a")  
timer = e32.Ao_timer()  
class LocFileSelector:
    def __init__(self,dir=".",ext='.jpg'):
        self.dir = unicode(dir)
        
        self.ext = ext
        self.files = {}
 
        def iter(fileselector,dir,files):
            for file in files:
                file=ru(file)
                b,e = os.path.splitext(file)
                if e == ".txt":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)
                if e == ".TXT":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)                 
                if e == ".ilktik":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)
                if e == ".ILKTIK":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)  
                if e == ".jpeg":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)
                if e == ".JPEG":
                    fileselector.files[u'%s' % b] = os.path.join(dir,file)   
        try:
            os.path.walk(self.dir,iter,self)
        except:
            pass
        self.sortedkeys = self.files.keys()
        self.sortedkeys.sort()
 
    def GetKeys(self):
        return self.sortedkeys
 
    def GetFile(self,index):
        return self.files[self.sortedkeys[index]]

def current_location():  
    gsm_loc = location.gsm_location()  
    return "%d/%d/%d/%d" % gsm_loc  
sirali="MCC/MNC/Area ID/Cell ID:"
def goster():
    timer.cancel()
    skalite=sysinfo.signal_dbm()
    mcc, mnc, area, cell = loc.split("/") 
    txt.set(ru(lang(1))+satir+ru(lang(91))+": "+loc+satir+ru(lang(92))+"(MCC): "+mcc+satir+ru(lang(93))+"(MNC): "+mnc+satir+ru(lang(94))+"(Area ID): "+area+satir+ru(lang(95))+" (Cell ID): "+cell+satir+ru(lang(96))+str(skalite))

    e32.ao_sleep(8)
    timer.after(INTERVAL, yenile)
satir="\n"
def standart_profil():
    profiles=[ru(lang(60)), ru(lang(61)), ru(lang(62)), ru(lang(63)), ru(lang(64)), ru(lang(65))]
    global standartprofile
    sp=appuifw.selection_list(choices=profiles)
    standartprofile=int(sp)+2
    kaydet()
        
def selectmusic():
    timer.cancel
    global musiclist
    musiclist=MusicSelector("E:\\Sounds",".mp3")
    global musiclisted
    musiclisted=musiclist.GetKeys()
    global musicindex
    musicindex=appuifw.selection_list(musiclisted, search_field=1) 
    global selected_music
    selected_music=musiclist.GetFile(musicindex)
    kaydet()
def kaysure():
    sureler=[ru("5 saniye"), ru("20 sn"), ru("45 sn"), ru("1 dk"), ru("2 dk")]
    global sures
    sures=appuifw.selection_list(choices=sureler)
    if sures==0:
        global sure
        sure=5
    if sures==1:
        global sure
        sure=20
    if sures==2:
        global sure
        sure=45
    if sures==3:
        global sure
        sure=60
    if sures==4:
        global sure
        sure=120
    kaydet()

standart=0
def dojob():
    f = file("E:\\System\\Apps\\CellLocation\\scells.ilktik", "r")
    global scellids
    scellids = {}  
    global signals
    signals = {}
    global status
    status = {}
    global actions
    actions = {}  
    global numbers
    numbers = {}
    global contents
    contents = {}  
    global senses
    senses = {}  
    for line in f:
        lockstat=PyKeyLock.LockStatus()
        key, value, signal, active, action, number, content, sense = line.split(":") 
        scellids[key.strip()] = eval(value.strip())
        signals[key.strip()] = int(signal.strip())
        status[key.strip()] = int(active.strip())
        actions[key.strip()] = action.strip()
        numbers[key.strip()] = number.strip()
        contents[key.strip()] = content.strip()
        senses[key.strip()] = int(sense.strip())
    f.close()
    global loc
    loc = current_location()
    global job
    job=1
    if loc in scellids:
        global here
        here = scellids[loc]
        max=signals[loc]+senses[loc]
        min=signals[loc]-senses[loc]
        now=sysinfo.signal_dbm()
        if now>=min:
            if now<=max:
                sinyalim=1
            else:
                sinyalim=0
        else:
            sinyalim=0
        if sinyalim==1:
            if actions[loc]=="Kapat":
                globalui.global_note(ru(lang(104)))
                e32.ao_sleep(20)
                switchoff.Shutdown()
            elif actions[loc]=="Profil":
                if loc!=yapildi:
                    if PyKeyLock.LockStatus()!=0:
                        PyKeyLock.Unlock(popup=0)
                        e32.ao_sleep(2)
                    appswitch.switch_to_bg(u'CellLocation')
                    simulate_key(63556,63556)
                    o=int(contents[loc])+1
                    i=0
                    while (i!=o):
                        e32.ao_sleep(0.2)
                        simulate_key(63498,63498)
                        i=i+1
                        e32.ao_sleep(0.1)
      
                    simulate_key(63557,63557)
                    global yapildi
                    yapildi=loc
                    global standart
                    standart=1

            elif actions[loc]=="Mesaj":
                if loc!=yapildi:
                    if standart==0:
                        messaging.sms_send(numbers[loc], contents[loc])
                        global standart
                        standart=1 
    try:    
        timer.after(INTERVAL, show_location)
    except:
        pass
def yenile():
    if olaylaretkin==1:
        dojob()

def show_location():  
    t=time()
    format_time(t)
    zaman=strftime('%d/%m/%Y-%H:%M')
    global loc
    loc = current_location()
    try:
        skalite = sysinfo.signal_dbm()
    except:
        skalite=0
    if loc in known_cells:  
        global here
        here = known_cells[loc]  
        txt.set(ru(lang(2))+satir+ru(lang(3))+here+satir+ru(lang(4))+satir+ru(lang(90))+": "+str(skalite)+satir+zaman)
    elif loc in known_cells2:  
        global here
        here = known_cells2[loc]
        txt.set(ru(lang(2))+satir+ru(lang(3))+here+satir+ru(lang(5))+satir+ru(lang(90))+": "+str(skalite)+satir+zaman)      
    else:
        global here  
        here = " "  
        txt.set(ru(lang(2))+satir+ru(lang(6))+satir+ru(lang(7))+satir+loc+satir+ru(lang(90))+": "+str(skalite)+satir+zaman)   
    yenile()      
    try:    
        timer.after(INTERVAL, show_location)
    except:
        pass

def name_location():
    bir=1
    iki=2
    uc=3
    dort=4
    loc = current_location()  
    timer.cancel()
    txt.set(ru(lang(8))+satir+ru(lang(9)))   
    e32.ao_sleep(4)
    name = appuifw.query(ru(lang(10)), "text")
    if name:
        colons = name.count(':')

        if colons > 0:
            appuifw.note(u"Cannot use ':' as part of location name.", "error")
            name=0

    if sysinfo.active_profile()=="offline":
        appuifw.note(ru(lang(78)), 'error')
        name=0
    if loc=="000/000/000/000":
        appuifw.note(ru(lang(79)), 'error')
        name=0  
    if name:
        i=0
        yukle=1
        locsayi=0
        bazk=[]
        while(sure!=i):
            loc = current_location()
            scellids[loc]=name
            signals[loc]=sysinfo.signal_dbm()
            status[loc]=0
            actions[loc]=u"kapali"
            numbers[loc]=0
            contents[loc]=0
            contents[loc]=0
            senses[loc]=100
            known_cells[loc] = name
            if loc in bazk:
                gec=1
            else:
                bazk.append(loc)
                locsayi=locsayi+1
            i=i+1
            kalan=sure-i
            if yukle==3:
                txt.set(ru(lang(80))+str(locsayi)+"\n"+ru(lang(81))+"...\n"+ru(lang(82))+"\n"+ru(lang(83))+str(kalan)+" "+ru(lang(84)))
                global yukle
                yukle=1
                e32.ao_sleep(1)
            if yukle==2:
                txt.set(ru(lang(80))+str(locsayi)+"\n"+ru(lang(81))+"..\n"+ru(lang(82))+"\n"+ru(lang(83))+str(kalan)+" "+ru(lang(84)))
                global yukle
                yukle=3
                e32.ao_sleep(1)
            if yukle==1:              
                txt.set(ru(lang(80))+str(locsayi)+"\n"+ru(lang(81))+".\n"+ru(lang(82))+"\n"+ru(lang(83))+str(kalan)+" "+ru(lang(84)))
                global yukle
                yukle=2

                e32.ao_sleep(1)
        txt.set(ru(lang(85)))
        save_dictionary(CELL_FILE, known_cells)
        save_scells()
        oku()
        appuifw.note(ru(lang(14))) 
        txt.set(ru(lang(15))+satir+ru(lang(16)))
        e32.ao_sleep(2)
    else:
        appuifw.note(ru(lang(86)))
        txt.set(ru(lang(87)))
    timer.after(INTERVAL, yenile)  
     
def load_cells():  
    global known_cells  
    try:  
        known_cells = load_dictionary(CELL_FILE)  
    except:  
        known_cells = {}
          
def load_cells2():  
    global known_cells2  
    try:  
        known_cells2 = load_dictionary(CLDB_FILE)  
    except:  
        known_cells2 = {}  
        
def load_dictionary(filename):  
    f = file(filename, "r")  
    global dict
    dict = {}  
    for line in f:  
        key, value = line.split(":") 
        dict[key.strip()] = eval(value.strip())
    f.close()   
    return dict

def load_scells(filename):  
    f = file(filename, "r")  
    global scellids
    scellids = {}  
    global signals
    signals = {}
    global status
    status = {}
    global actions
    actions = {}  
    global numbers
    numbers = {}
    global contents
    contents = {}  
    global senses
    senses = {}  
    for line in f:  
        key, value, signal, active, action, number, content, sense = line.split(":") 
        scellids[key.strip()] = eval(value.strip())
        signals[key.strip()] = int(signal.strip())
        status[key.strip()] = int(active.strip())
        actions[key.strip()] = action.strip()
        numbers[key.strip()] = number.strip()
        contents[key.strip()] = content.strip()
        senses[key.strip()] = int(sense.strip())
    f.close()

load_scells(SCELLS_FILE)

def save_dictionary(filename, dict):  
    f = file(filename, "w")  
    for key, value in dict.items():  
        print >> f, "%s: %s" % (key, repr(value), )  
    f.close()

def save_scells():  
    f = file(SCELLS_FILE, "w")  
    for key, value in scellids.items():  
        print >> f, "%s: %s: %s: %s: %s: %s: %s: %s" % (key, repr(value), signals[key], status[key], actions[key], numbers[key], contents[key], senses[key])  
    f.close()
 
def downloadyer():
    timer.cancel() 
    txt.set(ru(lang(17)))    
    URL = "http://www.ilktik.com/celllocation/icldb2.ilktik"
    dest_file = u"E:\\System\\Apps\\CellLocation\\icldb.ilktik"
    e32.ao_sleep(6)
    txt.set(ru(lang(18)))    
    urllib.urlretrieve(URL, dest_file)
    appuifw.note(ru(lang(19)), "info")
    e32.ao_sleep(1)
    timer.after(INTERVAL, yenile)
    
    
def uploadyer():
    timer.cancel()    
    filename = 'e:\\System\\Apps\\CellLocation\\known_cells.txt'
    picture = file(filename).read()
    txt.set(ru(lang(20)))
    e32.ao_sleep(6)
    txt.set(ru(lang(21)))
    e32.ao_sleep(6)
    txt.set(ru(lang(18)))
    conn = httplib.HTTPConnection("www.ilktik.com")
    conn.request("POST", "/celllocation/upload.php", picture)
    txt.set(ru(lang(22)))
    e32.ao_yield()
    response = conn.getresponse()
    remote_file = response.read()
    conn.close()
    appuifw.note(u" " + remote_file, "info")  
    txt.set(ru(lang(23)))      
    e32.ao_sleep(6)
    timer.after(INTERVAL, yenile)
    
def wikien():

    timer.cancel() 
    apprun = 'z:\\system\\programs\\apprun.exe'
    browser = 'z:\\System\\Apps\\Browser\\Browser.app'
    wikienurl='http://en.wikipedia.org/wiki/Search?go=Go&search='
    url = 'http://www.wikipedia.org'
    e32.start_exe(apprun, browser + ' "%s"' %url , 1)  

def wikitr():
    timer.cancel() 
    apprun = 'z:\\system\\programs\\apprun.exe'
    browser = 'z:\\System\\Apps\\Browser\\Browser.app'
    wikitrurl='http://tr.wikipedia.org/wiki/Search?fulltext=Ara&search='
    url = wikitrurl+here
    e32.start_exe(apprun, browser + ' "%s"' %url , 1)  
    
def googleen():
    timer.cancel() 
    apprun = 'z:\\system\\programs\\apprun.exe'
    browser = 'z:\\System\\Apps\\Browser\\Browser.app'
    googleenurl='http://www.google.com/search?hl=en&q='
    url =  googleenurl+here
    e32.start_exe(apprun, browser + ' "%s"' %url , 1)

def googletr():
    timer.cancel() 
    apprun = 'z:\\system\\programs\\apprun.exe'
    browser = 'z:\\System\\Apps\\Browser\\Browser.app'
    googletrurl='http://www.google.com.tr/search?hl=tr&q='
    url = googletrurl+here
    e32.start_exe(apprun, browser + ' "%s"' %url , 1)    

def dosyakaydet():
    try:
        e32.file_copy('E:\\Others\\known_cells.txt','E:\\System\\Apps\\CellLocation\\known_cells.txt')
        appuifw.note(ru(lang(24)), "info")
    except:
        appuifw.note(u"Error!", "error")
      
def quit():  
    txt.set(ru(lang(88)))  
    save_dictionary(CELL_FILE, known_cells)
    save_scells()
    timer.cancel()  
    log.close()  
    app_lock.signal()
    appswitch.end_app(u"CellLocation")
 
appuifw.app.exit_key_handler = arkaplan  
appuifw.app.title = u"IlkTik CellLocation"  
alanlar = {}

def alanlarim():
    f = file(CELL_FILE, "r")  
    
    dict = {}
    tersdict = {}  
    alanlistesi = []

    for line in f:  
        key, value = line.split(":") 
        dict[key.strip()] = eval(value.strip())
        tersdict[eval(value.strip())] = key.strip()
        alanlistesi.append(eval(value.strip()))

    index = appuifw.selection_list(alanlistesi, 1)
    yer = alanlistesi[index]
    yerid = ru(tersdict[yer])
    appuifw.note(yerid)
    e32.ao_sleep(5)

def duzenle():
    timer.cancel()
    f = file(CELL_FILE, "r")  
    
    dict = {}
    tersdict = {}  
    alanlistesi = []

    for line in f:  
        key, value = line.split(":") 
        dict[key.strip()] = eval(value.strip())
        tersdict[eval(value.strip())] = key.strip()
        alanlistesi.append(eval(value.strip()))
    f.close()
    index = appuifw.selection_list(alanlistesi, 1)
    yer = alanlistesi[index]
    yerid = ru(tersdict[yer])
    appuifw.note(yerid)
    name = appuifw.query(ru(lang(10)), "text")
    colons = name.count(':')
    if colons > 0:
        appuifw.note(u"Cannot use ':' as part of location name.", "error")
        name=0 

satir="\n"
bosluk=" "
def olaylar():
    timer.cancel()
    f = file(SCELLS_FILE, "r")  
    
    dict = {}
    tersdict = {}  
    alanlistesi = []

    for line in f:
        key, value, signal, active, action, number, content, sense = line.split(":") 
        dict[key.strip()] = eval(value.strip())
        tersdict[eval(value.strip())] = key.strip()
        
        alanlistesi.append(eval(value.strip()))
    f.close()
    index = appuifw.selection_list(alanlistesi, 1)
    yer = alanlistesi[index]
    yerid = ru(tersdict[yer])
    yapilacaklar=[ru(lang(51)), ru(lang(52)), ru(lang(53)), ru(lang(54))]
    simdiyap=appuifw.selection_list(choices=yapilacaklar)
    if simdiyap==0:
        txt.set(scellids[yerid]+satir+yerid+satir+actions[yerid])
        e32.ao_sleep(2)
        timer.after(INTERVAL, show_location)
    if simdiyap==1:
        name = appuifw.query(ru(lang(10)), "text")
        colons = name.count(':')
        if colons > 0:
            appuifw.note(u"Cannot use ':' as part of location name.", "error")
            name=0 
        if name:
            known_cells[yerid] = name 
            scellids[yerid] = name 
            appuifw.note(ru(lang(55)))        
            save_dictionary(CELL_FILE, known_cells)
            save_scells()
            load_cells2()
            load_cells()
            load_scells(SCELLS_FILE)
        e32.ao_sleep(2)
        timer.after(INTERVAL, show_location)
    if simdiyap==2:
        olaylistesi=[ru(lang(56)), ru(lang(57)), ru(lang(58)), ru(lang(59))]
        olay=appuifw.selection_list(choices=olaylistesi)
        if olay==0:
            actions[yerid]=u"Kapali"
            save_scells()
            load_scells(SCELLS_FILE)
            timer.after(INTERVAL, show_location)
        if olay==1:
            actions[yerid]=u"Kapat"
            save_scells()
            timer.after(INTERVAL, show_location)
        if olay==2:
            profiles=[ru(lang(60)), ru(lang(61)), ru(lang(62)), ru(lang(63)), ru(lang(64)), ru(lang(65))]

            sprofile=appuifw.selection_list(choices=profiles)
            actions[yerid]=u"Profil"
            contents[yerid]=int(sprofile)+1
            save_scells()
                  
            try:    
                timer.after(INTERVAL, show_location)
            except:
                pass
        if olay==3:
            actions[yerid]=u"Mesaj"
            telno = appuifw.query(ru(lang(66)), "text")
            if telno:
                mesaj = appuifw.query(ru(lang(67)), "text")
                colons = mesaj.count(':')
                if colons > 0:
                    appuifw.note(u"Cannot use ':' as part of location name.", "error")
                    mesaj=0
                if mesaj:
                    numbers[yerid]=telno
                    contents[yerid]=mesaj
                    actions[yerid]=u"Mesaj"

            
                    appuifw.note(ru(lang(68)))
                    save_scells()
                    load_scells(SCELLS_FILE)
                    try:    
                        timer.after(INTERVAL, show_location)
                    except:
                        pass

        if olay==4:
            selectmusic()
            actions[yerid]=u"Alarm"
            contents[yerid]=selected_music
            
            appuifw.note(ru(lang(89)))
            save_scells()
            load_scells(SCELLS_FILE)
            try:    
                timer.after(INTERVAL, show_location)
            except:
                pass

    if simdiyap==3:
        hasasliklistesi=[ru(lang(69)), ru(lang(70)), ru(lang(71)), ru(lang(72)), ru(lang(73)), ru(lang(74))]
        hsecim=appuifw.selection_list(choices=hasasliklistesi)
        if hsecim==0:
            senses[yerid]=100
            save_scells()
        if hsecim==1:
            senses[yerid]=40
            save_scells()
        if hsecim==2:
            senses[yerid]=30
            save_scells()
        if hsecim==3:
            senses[yerid]=20
            save_scells()
        if hsecim==4:
            senses[yerid]=10
            save_scells()
        if hsecim==5:
            senses[yerid]=6
            save_scells()
        load_scells(SCELLS_FILE)
        try:    
            timer.after(INTERVAL, show_location)
        except:
            pass
    if simdiyap==4:
        if (appuifw.query(scellids[yerid]+u"  olaylar listesinden silinsin mi?", 'query') == True):
            status[yerid]=0
    try:    
        timer.after(INTERVAL, show_location)
    except:
        pass


    
olaylaretkin=0
def calisma():
    if olaylaretkin==0:
        global olaylaretkin
        olaylaretkin=1
        appuifw.note(ru(lang(75)))
        yenile()
    elif olaylaretkin==1:
        global olaylaretkin
        olaylaretkin=0
        appuifw.note(ru(lang(76)))
        yenile()
def start_up():
    try:
        e32.file_copy("E:\\sw_autoexec\\CellLocation.aex", "E:\\System\\Apps\\CellLocation\\CellLocation.aex")
    except:
        pass
    try:
        e32.file_copy("E:\\System\\sw_autoexec\\CellLocation.aex", "E:\\System\\Apps\\CellLocation\\CellLocation.aex")
    except:
        pass
    appuifw.note(ru(lang(100)))

def not_start_up():
    try:
        os.remove("E:\\sw_autoexec\\CellLocation.aex")
    except:
        pass
    try:
        os.remove("E:\\System\\sw_autoexec\\CellLocation.aex")
    except:
        pass

    appuifw.note(ru(lang(101)))
def arastir():
    params = urllib.urlencode({'yer': here})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("www.ilktik.com")
    conn.request("POST", "/celllocation/arastir.php", params, headers)
    response = conn.getresponse()
    yanit = response.read()
    if yanit=="internalerror":
        txt.set(ru("Error on server, remote service is updating..."))
    e32.file_copy("E:\\System\\Apps\\CellLocation\\research.html", "E:\\System\\Apps\\CellLocation\\iservice")
    f = file("E:\\System\\Apps\\CellLocation\\research.html", "w") 
    print >> f, yanit 
    f.close()
    e32.start_exe('z:\\system\\programs\\apprun.exe','z:\\system\\apps\\browser\\browser.app "file://E:/System/Apps/CellLocation/research.html"')
    e32.ao_sleep(1)
    e32.start_exe('z:\\system\\programs\\apprun.exe','z:\\system\\apps\\browser\\browser.app "file://E:/System/Apps/CellLocation/research.html"')


txt.set(ru("(C) İlkTık.com.\n Do not redistribute, share, edit or include to other programs.\nUygulamayı tekrar dağıtmayın, düzenlemeyin ya da başka bir programa dahil etmeyin."))  
load_cells2()
load_cells()
sayipre = len(known_cells)
sayi = str(sayipre)
sayipre2 = len(known_cells2)
sayidb = str(sayipre2)
version = "Surum"
if version in known_cells2:  
    surum = known_cells2[version]
else:
    surum=ru(lang(32))        
txt.set(ru(lang(33))+satir+ru(lang(34))+bosluk+sayi+bosluk+ru(lang(35))+satir+satir+ru(lang(36))+bosluk+sayidb+bosluk+ru(lang(37))+ru(lang(39)))
e32.ao_sleep(1) 
appuifw.app.menu = [(ru(lang(40)), ((ru(lang(27)), name_location), (ru(lang(41)), goster), (ru(lang(42)), arastir))), (ru(lang(43)), olaylar), (ru(lang(44)), ((ru(lang(45)),arkaplan),(ru(lang(46)), calisma))), (ru(lang(47)), ((ru(lang(29)), uploadyer), (ru(lang(30)), dosyakaydet), (ru(lang(31)), downloadyer))), (ru(lang(97)), ((ru(lang(98)), start_up), (ru(lang(99)), not_start_up))), (ru(lang(48)), ((ru("Language"), dilsec), (ru(lang(50)), kaysure))), (ru(lang(103)), hakkinda), ((ru(lang(106))), quit)] 
timer.after(INTERVAL, yenile)
global olaylaretkin
olaylaretkin=1
appuifw.note(ru(lang(102)))
appswitch.switch_to_bg(u'CellLocation')
app_lock = e32.Ao_lock()  
app_lock.signal()
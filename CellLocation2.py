import appuifw, e32, location, time, os, httplib, urllib, appswitch, sysinfo, messaging, switchoff, PyKeyLock, thread
appuifw.app.screen='normal'
from keypress import simulate_key 

appuifw.app.title=u'CellLocation'
def ru(x):return x.decode('utf-8') 
txt = appuifw.Text()
appuifw.app.body = txt
appuifw.app.body.color = (0,
 0,
 0) 
yapildi=0 
lockey=0
bosluk=" "
def kaydet():
    CONFIG_DIR='E:/System/Apps/CellLocation'
    CONFIG_FILE=os.path.join(CONFIG_DIR,'mysettings.txt')
    if not os.path.isdir(CONFIG_DIR):
        os.makedirs(CONFIG_DIR)
        CONFIG_FILE=os.path.join(CONFIG_DIR,'mysettings.txt')      
    config={}
    config['variable1']= prgdili
    config['sp']= standartprofile        
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
        except:
            print 'dosya okunamiyor'
    except:
        print 'dosya acilamiyor'
oku()

try:
   appswitch.end_app(u"Kamera")
except:
   pass

try:
   appswitch.end_app(u"Camera")
except:
   pass


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
    

if sysinfo.active_profile()==u"offline":
    appuifw.note(ru("Hatsız tercihinde yer bilgisi alınamaz..."))
         
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
    txt.set(ru(lang(1))+satir+ru("Konum Bilgisi:")+loc+satir+ru("Ülke Kodu (MCC): ")+mcc+satir+ru("Şebeke Kodu (MNC): ")+mnc+satir+ru("Alan Kodu(Area ID): ")+area+satir+ru("Hücre Kodu (Cell ID): ")+cell+satir+ru("Sinyal Gücü:")+str(skalite))

    e32.ao_sleep(8)
    timer.after(INTERVAL, yenile)
satir="\n"
def standart_profil():
    profiles=[ru("Genel"), ru("Sessiz"), ru("Toplanti"), ru("Dış Mekan"), ru("Çağrı"), ru("Hatsız(CL Durur)")]
    global standartprofile
    standartprofile=appuifw.selection_list(choices=profiles)
    kaydet()
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
                switchoff.Shutdown()
            elif actions[loc]=="Profil":
                if loc!=yapildi:
                    if PyKeyLock.LockStatus()==0:   
                        appswitch.switch_to_bg(u'Python')
                        simulate_key(63556,63556)
                        prei=contents[loc]
                        o=prei
                        o=int(o)+2
                        i=0
                        while (i!=o):
                            e32.ao_sleep(0.1)
                            simulate_key(63498,63498)
                            i=i+1
                        
                        e32.ao_sleep(0.1)
                        simulate_key(63557,63557)
                        global yapildi
                        yapildi=loc
                        global standart
                        standart=0
                        appswitch.switch_to_fg(u'Python')
                        if lockey==1:
                            PyKeyLock.Lock(1)
                    else:
                        PyKeyLock.Unlock(0)
                        global lockey
                        lockey=1
                if yapildi!=loc:        
                    if standart==0:
                        if PyKeyLock.LockStatus()==0:   
                            appswitch.switch_to_bg(u'Python')
                            simulate_key(63556,63556)
                            prei=contents[loc]
                            o=int(standartprofile)
                            o=o+2
                            i=0
                            while (i!=o):
                                e32.ao_sleep(0.1)
                                simulate_key(63498,63498)
                                i=i+1
                        
                            e32.ao_sleep(0.1)
                            simulate_key(63557,63557)
                            global yapildi
                            yapildi=loc
                            appswitch.switch_to_fg(u'Python')
                            if lockey==1:
                                PyKeyLock.Lock(1)
                        else:
                            PyKeyLock.Unlock(0)
                            global lockey
                            lockey=1
            elif actions[loc]=="Mesaj":
                if loc!=yapildi:
                    if standart==0:
                        messaging.sms_send(numbers[loc], contents[loc])
                        global standart
                        standart=1  
    
    timer.after(INTERVAL, yenile)    
def show_location():  
    global loc
    loc = current_location()
    skalite = sysinfo.signal_dbm()
    if loc in known_cells:  
        global here
        here = known_cells[loc]  
        txt.set(ru(lang(2))+satir+ru(lang(3))+here+satir+ru(lang(4))+satir+ru("Sinyal Kalitesi: ")+str(skalite))
    elif loc in known_cells2:  
        global here
        here = known_cells2[loc]
        txt.set(ru(lang(2))+satir+ru(lang(3))+here+satir+ru(lang(5))+satir+ru("Sinyal Kalitesi: ")+str(skalite))      
    else:
        global here  
        here = " "  
        txt.set(ru(lang(2))+satir+ru(lang(6))+satir+ru(lang(7))+satir+loc+satir+ru("Sinyal Kalitesi: ")+str(skalite))   
      
    print >> log, time.ctime(), loc, repr(here)  

    timer.after(INTERVAL, yenile)
def yenile():
    if olaylaretkin==1:
        dojob()
    show_location()
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
        appuifw.note(ru("Hatsız tercinde kayıt yapılamaz."), 'error')
        name=0
    if loc=="000/000/000/000":
        appuifw.note(ru("Şebeke bağlantısı sorunlu. Kayıt yapılamaz."), 'error')
        name=0
    if name:
        scellids[loc]=name
        signals[loc]=sysinfo.signal_dbm()
        status[loc]=0
        actions[loc]=u"kapali"
        numbers[loc]=0
        contents[loc]=0
        contents[loc]=0
        senses[loc]=30
        known_cells[loc] = name    
        appuifw.note(ru(lang(11))) 
        txt.set(ru(lang(12))+ru(lang(13))+unicode(iki))
        e32.ao_sleep(10)
        loc = current_location()
    else:
        appuifw.note(u"Name is not acceaptable.") 
    if name:      
        scellids[loc]=name
        signals[loc]=sysinfo.signal_dbm()
        status[loc]=0
        actions[loc]=u"kapali"
        numbers[loc]=0
        contents[loc]=0
        contents[loc]=0
        senses[loc]=30
        known_cells[loc] = name
        appuifw.note(ru(lang(11))) 
        txt.set(ru(lang(12))+ru(lang(13))+unicode(uc))
        e32.ao_sleep(10)
        loc = current_location()  
    if name:      
        scellids[loc]=name
        signals[loc]=sysinfo.signal_dbm()
        status[loc]=0
        actions[loc]=u"kapali"
        numbers[loc]=0
        contents[loc]=0
        contents[loc]=0
        senses[loc]=30
        known_cells[loc] = name
        appuifw.note(ru(lang(11)))   
        txt.set(ru(lang(12))+ru(lang(13))+unicode(dort))
        e32.ao_sleep(10)
        loc = current_location()  
    if name:      
        scellids[loc]=name
        signals[loc]=sysinfo.signal_dbm()
        status[loc]=0
        actions[loc]=u"kapali"
        numbers[loc]=0
        contents[loc]=0
        contents[loc]=0
        senses[loc]=30
        known_cells[loc] = name
        appuifw.note(ru(lang(14))) 
        txt.set(ru(lang(15))+satir+ru(lang(16)))
        e32.ao_sleep(4)
    save_dictionary(CELL_FILE, known_cells)
    save_scells()
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
    txt.set(ru("Çıkış şu anda gerçekleştirilemedi. Çalışan bir işlem ya da hata olabilir.\n\nLütfen bekleyin...\nUzun sürerse kırmızı kapatma tuşuna basın."))  
    save_dictionary(CELL_FILE, known_cells)
    save_scells()
    txt.set(ru(lang(26)))
    timer.cancel()  
    log.close()  
    app_lock.signal()
    appswitch.end_app(u"CellLocation")
  
appuifw.app.exit_key_handler = quit  
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
    yapilacaklar=[u'Alan Bilgisi', ru('Yeniden Adlandır'), u'Alana Olay Ata', ru('Hassaslık Ayarı')]
    simdiyap=appuifw.selection_list(choices=yapilacaklar)
    if simdiyap==0:
        txt.set(scellids[yerid]+satir+yerid+satir+actions[yerid])
        e32.ao_sleep(2)
        timer.after(INTERVAL, yenile)
    if simdiyap==1:
        name = appuifw.query(ru(lang(10)), "text")
        colons = name.count(':')
        if colons > 0:
            appuifw.note(u"Cannot use ':' as part of location name.", "error")
            name=0 
        if name:
            known_cells[yerid] = name 
            scellids[yerid] = name 
            appuifw.note(ru("Alanlar Yükleniyor..."))        
            save_dictionary(CELL_FILE, known_cells)
            save_scells()
            load_cells2()
            load_cells()
            load_scells(SCELLS_FILE)
        e32.ao_sleep(2)
        timer.after(INTERVAL, yenile)
    if simdiyap==2:
        olaylistesi=[u'Kapali', u'Telefonu Kapat', u'Profili Degistir', u'Mesaj Gonder']
        olay=appuifw.selection_list(choices=olaylistesi)
        if olay==0:
            actions[yerid]=u"Kapali"
            save_scells()
            load_scells(SCELLS_FILE)
            timer.after(INTERVAL, yenile)
        if olay==1:
            actions[yerid]=u"Kapat"
            save_scells()
            timer.after(INTERVAL, yenile)
        if olay==2:
            profiles=[ru("Genel"), ru("Sessiz"), ru("Toplanti"), ru("Dış Mekan"), ru("Çağrı"), ru("Hatsız(CL Durur)")]

            sprofile=appuifw.selection_list(choices=profiles)
            actions[yerid]=u"Profil"
            contents[yerid]=sprofile
            save_scells()
            timer.after(INTERVAL, yenile)
        if olay==3:
            actions[yerid]=u"Mesaj"
            telno = appuifw.query(ru("Telefon Numarasi"), "number")
            if telno:
                mesaj = appuifw.query(ru("Mesaji Girin"), "text")
                colons = mesaj.count(':')
                if colons > 0:
                    appuifw.note(u"Cannot use ':' as part of location name.", "error")
                    mesaj=0
                if mesaj:
                    numbers[yerid]=telno
                    contents[yerid]=mesaj
                    actions[yerid]=u"Mesaj"
                    appuifw.note(ru("İsteğiniz gerçekleştiriliyor..."))
                    save_scells()
                    load_scells(SCELLS_FILE)

                    timer.after(INTERVAL, yenile)
    if simdiyap==3:
        txt.set(ru("Hasaslık Düzeyi kaydedilen hücre İçindeki konumunuzu daha net tespit etmek icin sinyal oranini kullanir. Telefonu yatay ya da dikey olarak hareket ettirmek, cebinize koymak ya da asansöre binmek sinyal oranını değiştirir. Ayni hücre içinde olduğunuzda yanilsama olabilir."))
        e32.ao_sleep(5)
        hasasliklistesi=[u'Hucrenin Tumu', u'Dusuk', u'Orta', u'Yuksek', u'Cok Yuksek', u'En Yuksek']
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
        timer.after(INTERVAL, yenile)
    if simdiyap==4:
        if (appuifw.query(scellids[yerid]+u"  olaylar listesinden silinsin mi?", 'query') == True):
            status[yerid]=0
def arkaplan():
    appswitch.switch_to_bg(u"Python")
olaylaretkin=0
def calisma():
    if olaylaretkin==0:
        global olaylaretkin
        olaylaretkin=1
        appuifw.note(ru("Olaylar etkin. Uygulamayi arkaplana alın."))
        yenile()
    elif olaylaretkin==1:
        global olaylaretkin
        olaylaretkin=0
        appuifw.note(ru("Olaylar etkin değil."))
        yenile()
def arastir():
    params = urllib.urlencode({'yer': loc})
    headers = {"Content-type": "application/x-www-form-urlencoded","Accept": "text/plain"}
    conn = httplib.HTTPConnection("www.ilktik.com")
    conn.request("POST", "/celllocation/arastir.php", params, headers)
    response = conn.getresponse()
    yanit = response.read()
    if yanit=="internalerror":
        txt.set(ru("bir hata olustu"))

txt.set(ru("All rights reserved. İlkTık.com.\n Do not redistribute, share, edit or include to other programs.\
"))  
load_cells2()
load_cells()
e32.ao_sleep(1) 
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

appuifw.app.menu = [(ru("Bulunduğum Yer"), ((ru(lang(27)), name_location), (ru("Alan Bilgisini Göster"), goster), (ru("Bilgi ve Harita"), arastir))), (ru("Alanlar ve Olaylar"), olaylar), (ru("Uygulama"), ((ru("Arkaplanda Çalış"),arkaplan),(ru("Olayları Aç/Kapat"), calisma))), (ru("Veritabanı İşlemleri"), ((ru(lang(29)), uploadyer), (ru(lang(30)), dosyakaydet), (ru(lang(31)), downloadyer))), (ru("Ayarlar"), ((ru("Lang.Sprech.Dil."), dilsec), (ru("Standart Profil"), standart_profil)))] 
timer.after(INTERVAL, yenile)
app_lock = e32.Ao_lock()  
app_lock.wait()
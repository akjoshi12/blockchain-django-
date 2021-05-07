from datetime import datetime
import hashlib
from django.shortcuts import render
from django.shortcuts import render, redirect
from block0.models import BlockDetails , transaction , User
# Create your views here.

def nonce(fhash):
    a = fhash
    has = a.encode()
    has = hashlib.sha256(has)
    has = has.hexdigest()
    n = 0
    x = 0
    for i in range(0,10000000,1):
 
        k = str(i)
        has = k+has
        has = has.encode()
        has = hashlib.sha256(has)
        has = has.hexdigest()

        if(has.startswith('000')):
            x = has
            n = i
            break
      
    return(x,n)

def merkle_root(ar):
    a = ar
    n = len(a)
    b = n-1
    while(n>1):
        x = len(a)
        y = x-1
        if((len(a))%2!=0):
            a.append(a[y])
  
        n1 = int(len(a)/2)
        arr = []
        j = 0
        while(n1>0):
            arr.append(a.pop())
            arr[j]+=a.pop()
            has = arr[j].encode()
            has = hashlib.sha256(has)
            has = has.hexdigest()
            arr[j] = has
            j = j+1
            n1 = n1-1
    
        a = arr
        a.reverse()
        n = n/2
    return str(a[0])

def home(request):
    return render (request,'index.html')

def login(request):
    a = 'login.html'
    context = {"message":" "}
    if request.method == "POST":
        pub = request.POST.get('pubkey')
        priv = request.POST.get('privkey')
        form = User.objects.get(pub=pub,priv=priv)
        if(form.pub==pub and form.priv==priv):
            a = 'index.html'
        else:
            return redirect ('login')
            a = 'login.html'
            context = {"message":"Pulic or Private key is invalid"}
    return render (request,a,context)

def steps(request):
    print("hello")
    return render (request,'steps.html')

def about(request):
    return render (request ,'about.html')

def transactions(request):
    count = 0
    context = {"message":"Privacy Simplified"}
    res = 0 
    no = transaction.objects.raw('select block_no as id, count(*) from block0_transaction group by block_no having count(*) < 3 and block_no != 0')
    
    if(len(no) <= 0):
        res = transaction.objects.raw('select 1 as id, COALESCE(max(block_no)+1,1) as new_block_no from block0_transaction')
        new_block_no = int(res[0].new_block_no)
        x = new_block_no-1
        trans1 = transaction.objects.filter(block_no=x)
        arr = []
        
        for i in trans1:
            arr.append(i.current_hash)
        
        now = datetime.now()
        timestamp = datetime.timestamp(now)
        mr = merkle_root(arr)        
        prev_hash = BlockDetails.objects.raw('''SELECT  id, finalhash , block FROM block0_BlockDetails ORDER BY id DESC LIMIT 1''')
        fhash = str(mr+str(timestamp)+str(x)+prev_hash[0].finalhash)
        (fhash,non) = nonce(fhash)
        a = prev_hash[0].block
        a = int(a)
        if (a==new_block_no-1):
            print("block already exists")
        else:
            blk = BlockDetails.objects.create(block=new_block_no-1,nonce=non,merkleroot=mr,previous_hash=prev_hash[0].finalhash,finalhash=fhash,timestamp=timestamp)
            blk.save()
    else :
        res = transaction.objects.raw('select 1 as id, COALESCE(max(block_no),1) as new_block_no from block0_transaction')
        new_block_no = int(res[0].new_block_no)

    if request.method == 'POST':
        r_pub_key = request.POST.get('r_public_key')
        s_pub_key = request.POST.get('s_public_key')
        s_priv_key = request.POST.get('s_private_key')
        amount = request.POST.get('amount')
        now = datetime.now()
        timestamp = datetime.timestamp(now) 
        has = r_pub_key+s_pub_key+amount+str(timestamp)
        has = has.encode()
        has = hashlib.sha256(has)
        has = has.hexdigest()
        amount = int(amount)
        data = User.objects.get(pub=s_pub_key,priv=s_priv_key)
        
        if (data.balance >= amount):
            trans = transaction.objects.create(r_pub=r_pub_key,s_pub=s_pub_key,amount=amount,current_hash=has,block_no=new_block_no)       
            
            a = data.balance-amount
            b = User.objects.get(pub=r_pub_key)
            b.balance = b.balance+amount
            c = b.balance
            User.objects.filter(priv=s_priv_key).update(balance=a)
            User.objects.filter(pub=r_pub_key).update(balance=c)
            trans.save()
            context = {"message":"Transaction Sucessfull"}
        else :
            context={"message":"Transaction Failed Not enough money"}
    return render(request,'transaction.html',context)

def quotes(request):
    return render(request,'quotes.html')

def history(request):
    blockdetails  = BlockDetails.objects.all()
    transdetails = transaction.objects.all()
    context = {'blkdetails':blockdetails , 'transdetails':transdetails}
    return render(request,'transaction_history.html',context)

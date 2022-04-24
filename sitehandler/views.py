from django.http import request, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import User, Group
from .models import *
from django.contrib.auth import authenticate, logout, login
from django.utils import timezone
from django.core.mail import EmailMessage, send_mail
from django.conf import settings


def homepage(request):
    return render(request, 'index.html')


def aboutpage(request):
    return render(request, 'about.html')


def contact(request):
    return render(request, 'contact.html')


def viewdoctor(request):
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request, 'viewdoctor.html', d)


def Login_admin(request):
    error = ""
    if request.method == 'POST':
        u = request.POST['username']
        p = request.POST['password']
        user = authenticate(username=u, password=p)
        try:
            if user.is_staff:
                login(request, user)
                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'adminlogin.html', d)


def loginpage(request):
    error = ""
    page = ""
    if request.method == 'POST':
        u = request.POST['email']
        p = request.POST['password']
        user = authenticate(request, username=u, password=p)
        try:
            if user is not None:
                login(request, user)
                error = "no"
                g = request.user.groups.all()[0].name
                if g == 'Doctor':
                    page = "doctor"
                    d = {'error': error, 'page': page}
                    return render(request, 'doctorhome.html', d)
                elif g == 'Receptionist':
                    page = "reception"
                    d = {'error': error, 'page': page}
                    return render(request, 'receptionhome.html', d)
                elif g == 'Patient':
                    page = "patient"
                    d = {'error': error, 'page': page}
                    return render(request, 'patienthome.html', d)
            else:
                error = "yes"
        except Exception as e:
            error = "yes"

    return render(request, 'login.html')


def createaccountpage(request):
    error = ""
    user = "none"
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        bloodgroup = request.POST['bloodgroup']
        try:
            if password == repeatpassword:
                Patient.objects.create(name=name, email=email, password=password, gender=gender, phonenumber=phonenumber, address=address, birthdate=birthdate, bloodgroup=bloodgroup)
                user = User.objects.create_user(first_name=name, email=email, password=password, username=email)
                pat_group = Group.objects.get(name='Patient')
                pat_group.user_set.add(user)
                user.save()

                error = "no"
            else:
                error = "yes"
        except Exception as e:
            error = "yes"
        # print("Error:",e)
    d = {'error': error}

    return render(request, 'createaccount.html', d)


def adminaddDoctor(request):
    error = ""
    user = "none"
    if not request.user.is_staff:
        return redirect('login_admin')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpasssword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        bloodgroup = request.POST['bloodgroup']
        specialization = request.POST['specialization']

        try:
            if password == repeatpassword:
                Doctor.objects.create(name=name, email=email, password=password, gender=gender, phonenumber=phonenumber, address=address, birthdate=birthdate, bloodgroup=bloodgroup, specialization=specialization)
                user = User.objects.create_user(first_name=name, email=email, password=password, username=email)
                doc_group = Group.objects.get(name='Doctor')
                doc_group.user_set.add(user)
                user.save()
                error = "no"
            else:
                error = "yes"
        except Exception as e:
            error = "yes"
    d = {'error': error}
    return render(request, 'adminadddoctor.html', d)


def adminviewDoctor(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    doc = Doctor.objects.all()
    d = {'doc': doc}
    return render(request, 'adminviewDoctors.html', d)


def admin_delete_doctor(request, pid, email):
    if not request.user.is_staff:
        return redirect('login_admin')
    doctor = Doctor.objects.get(id=pid)
    doctor.delete()
    users = User.objects.filter(username=email)
    users.delete()
    return redirect('adminviewDoctor')


def adminviewPatient(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    pat = Patient.objects.all()
    d = {'pat': pat}

    return render(request, 'adminviewPatient.html', d)


def admin_delete_patient(request, pid, email):
    if not request.user.is_active:
        return redirect('login_admin')
    patient = Patient.objects.get(id=pid)
    patient.delete()
    users = User.objects.filter(username=email)
    users.delete()
    return redirect('adminviewPatient')


def patient_delete_appointment(request, pk):
    appointment = Appointment.objects.get(id=pk)
    appointment.delete()
    return redirect('viewappointments')


def adminaddReceptionist(request):
    error = ""
    if not request.user.is_staff:
        return redirect('login_admin')

    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        repeatpassword = request.POST['repeatpassword']
        gender = request.POST['gender']
        phonenumber = request.POST['phonenumber']
        address = request.POST['address']
        birthdate = request.POST['dateofbirth']
        bloodgroup = request.POST['bloodgroup']

        try:
            if password == repeatpassword:
                Receptionist.objects.create(name=name, email=email, password=password, gender=gender, phonenumber=phonenumber, address=address, birthdate=birthdate, bloodgroup=bloodgroup)
                user = User.objects.create_user(first_name=name, email=email, password=password, username=email)
                rec_group = Group.objects.get(name='Receptionist')
                rec_group.user_set.add(user)

                user.save()

                error = "no"
            else:
                error = "yes"
        except:
            error = "yes"
    d = {'error': error}
    return render(request, 'adminaddreceptionist.html', d)


def adminviewReceptionist(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    rec = Receptionist.objects.all()
    r = {'rec': rec}
    return render(request, 'adminviewreceptionists.html', r)


def admin_delete_receptionist(request, pid, email):
    if not request.user.is_staff:
        return redirect('login_admin')
    reception = Receptionist.objects.get(id=pid)
    reception.delete()
    users = User.objects.filter(username=email)
    users.delete()
    return redirect('adminviewReceptionist')


def adminviewAppointment(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    upcomming_appointments = Appointment.objects.filter(appointmentdate__gte=timezone.now(), status=True).order_by('appointmentdate')
    previous_appointments = Appointment.objects.filter(appointmentdate__lt=timezone.now()).order_by( '-appointmentdate') | Appointment.objects.filter(status=False).order_by('-appointmentdate')
    d = {"upcomming_appointments": upcomming_appointments, "previous_appointments": previous_appointments}
    return render(request, 'adminviewappointments.html', d)


def Logout(request):
    if not request.user.is_active:
        return redirect('loginpage')
    logout(request)
    return redirect('loginpage')


def Logout_admin(request):
    if not request.user.is_staff:
        return redirect('login_admin')
    logout(request)
    return redirect('login_admin')


def AdminHome(request):
    # after login user comes to this page.
    totalpatients = Patient.objects.all()
    totaldoctors = Doctor.objects.all()
    totalreceptionists = Receptionist.objects.all()
    totalappointments = Appointment.objects.all()
    totalpatient = totalpatients.count()
    totaldoctor = totaldoctors.count()
    totalreceptionist = totalreceptionists.count()
    totalappointment = totalappointments.count()
    context = {'totalpatients': totalpatient, 'totaldoctors': totaldoctor, 'totalreceptionists': totalreceptionist, 'totalappointments': totalappointment}
    if not request.user.is_staff:
        return redirect('login_admin')

    return render(request, 'adminhome.html', context)


def Home(request):
    if not request.user.is_active:
        return redirect('loginpage')

    g = request.user.groups.all()[0].name

    if g == 'Doctor':
        pat = Patient.objects.all()
        p = {'pat': pat}
        return render(request, 'doctorhome.html', p)

    elif g == 'Receptionist':
        pat = Patient.objects.all()
        p = {'pat': pat}
        return render(request, 'receptionhome.html', p)

    elif g == 'Patient':
        return render(request, 'patienthome.html')


def profile(request):
    if not request.user.is_active:
        return redirect('loginpage')

    g = request.user.groups.all()[0].name
    if g == 'Patient':
        patient_detials = Patient.objects.all().filter(email=request.user)
        d = {'patient_detials': patient_detials}
        return render(request, 'pateintprofile.html', d)
    elif g == 'Doctor':
        doctor_detials = Doctor.objects.all().filter(email=request.user)
        d = {'doctor_detials': doctor_detials}
        return render(request, 'doctorprofile.html', d)
    elif g == 'Receptionist':
        reception_details = Receptionist.objects.all().filter(email=request.user)
        d = {'reception_details': reception_details}
        return render(request, 'receptionprofile.html', d)


def MakeAppointments(request):
    error = ""
    if not request.user.is_active:
        return redirect('loginpage')
    alldoctors = Doctor.objects.all()
    d = {'alldoctors': alldoctors}
    g = request.user.groups.all()[0].name
    if g == 'Patient':
        if request.method == 'POST':
            doctoremail = request.POST['doctoremail']
            doctorname = request.POST['doctorname']
            patientname = request.POST['patientname']
            patientemail = request.POST['patientemail']
            appointmentdate = request.POST['appointmentdate']
            appointmenttime = request.POST['appointmenttime']
            symptoms = request.POST['symptoms']

            send_mail(
                'Reminder for appointment',
                'Your Appointment details are =  ' + "Doctor name: " + doctorname + ", Appointment Date: " + appointmentdate + "and Appointment Time: " + appointmenttime,
                settings.EMAIL_HOST_USER,
                [patientemail],
                fail_silently=False,
            )

            try:
                Appointment.objects.create(doctorname=doctorname, doctoremail=doctoremail, patientname=patientname, patientemail=patientemail, appointmentdate=appointmentdate, appointmenttime=appointmenttime, symptoms=symptoms, status=True, prescription="")
                error = "no"
            except:
                error = "yes"
            e = {"error": error}
            return render(request, 'pateintmakeappointments.html', e)
        elif request.method == 'GET':
            return render(request, 'pateintmakeappointments.html', d)


def viewappointments(request):
    if not request.user.is_active:
        return redirect('loginpage')

    g = request.user.groups.all()[0].name
    if g == 'Patient':
        upcomming_appointments = Appointment.objects.filter(patientemail=request.user, appointmentdate__gte=timezone.now(), status=True).order_by('appointmentdate')
        previous_appointments = Appointment.objects.filter(patientemail=request.user,appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(patientemail=request.user, status=False).order_by('-appointmentdate')
        for i in upcomming_appointments:
            print(i.doctorname)

        d = {"upcomming_appointments": upcomming_appointments, "previous_appointments": previous_appointments}
        return render(request, 'patientviewappointments.html', d)
    elif g == 'Doctor':
        if request.method == 'POST':
            prescriptiondata = request.POST['prescription']
            idvalue = request.POST['idofappointment']
            Appointment.objects.filter(id=idvalue).update(prescription=prescriptiondata, status=False)

        upcomming_appointments = Appointment.objects.filter(appointmentdate__gte=timezone.now(), status=True).order_by('appointmentdate')
        previous_appointments = Appointment.objects.filter(doctoremail=request.user,appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(doctoremail=request.user,status=False).order_by('-appointmentdate')
        d = {"upcomming_appointments": upcomming_appointments, "previous_appointments": previous_appointments}
        return render(request, 'doctorviewappointment.html', d)
    elif g == 'Receptionist':
        upcomming_appointments = Appointment.objects.filter(appointmentdate__gte=timezone.now(), status=True).order_by('appointmentdate')
        previous_appointments = Appointment.objects.filter(appointmentdate__lt=timezone.now()).order_by('-appointmentdate') | Appointment.objects.filter(status=False).order_by('-appointmentdate')
        d = {"upcomming_appointments": upcomming_appointments, "previous_appointments": previous_appointments}
        return render(request, 'receptionviewappointments.html', d)

# class SubmitNormForm(TemplateView):
#     template_name = 'index.html'

#     def post(self, request, *args, **kwargs):
#         if not self.request.user.groups.filter(name='Admins').exists():
#             return redirect('/')
#         context = self.get_context_data(**kwargs)
#         # create a form instance and populate it with data from the request:
#         form = NormFormForm(request.POST)

#         # Create Preview if indicated
#         if 'preview' in request.POST and request.POST.get('preview'):
#             if form.is_valid():
#                 form_to_save = form.save(commit=False)
#                 form_to_save.created_by = request.user
#                 form_to_save.filename = f'preview - {form_to_save.date} - {form_to_save.patient} - ' \
#                                         f'{form_to_save.facility} ' + str(uuid.uuid4()) + '.pdf'

#                 # Save to PDF
#                 print('Processing NormForm to PDF now... '
#                       f'preview - {form_to_save.date} - {form_to_save.patient} - {form_to_save.facility}')
#                 filename = os.path.abspath(
#                     os.path.dirname(__file__)) + '/patient_files/preview/' + form_to_save.filename
#                 signature = form.cleaned_data.get('signature')
#                 if signature:
#                     signature_file_path = draw_signature(signature, as_file=True)
#                 else:
#                     raise FileExistsError("No signature file found")
#                 flowable_form_builder.build_form(form_to_save=form_to_save, filename=filename,
#                                                  signature_file_path=signature_file_path)
#                 return FileResponse(open(os.path.abspath(os.path.dirname(__file__)) +
#                                          '/patient_files/preview/' +
#                                          form_to_save.filename, 'rb'), content_type='application/pdf')
#         else:
#             if form.is_valid():
#                 # Save to DB
#                 form_to_save = form.save(commit=False)
#                 form_to_save.created_by = request.user
#                 form_to_save.filename = f'{form_to_save.date} - {form_to_save.patient} - ' \
#                                         f'{form_to_save.facility} ' + str(uuid.uuid4()) + '.pdf'
#                 form_to_save.save()
#                 messages.add_message(request, messages.SUCCESS, "Successfully saved form.")
#                 print('saved successfully')

#                 # Save to PDF
#                 print('Processing NormForm to PDF now... '
#                       f'{form_to_save.patient} - {form_to_save.facility} - {form_to_save.date}')
#                 filename = os.path.abspath(os.path.dirname(__file__)) + '/patient_files/' + form_to_save.filename
#                 # pdf = canvas.Canvas(filename=os.path.abspath(os.path.dirname(__file__)) + '/patient_files/' + filename,
#                 #                     pagesize=letter)
#                 signature = form.cleaned_data.get('signature')
#                 if signature:
#                     # as an image
#                     # signature_picture = draw_signature(signature)
#                     # or as a file
#                     signature_file_path = draw_signature(signature, as_file=True)
#                     # Might be a corner case here when nothing is entered into field on second
#                     # entry after a long time when tmp files have been purged
#                 else:
#                     raise FileExistsError("No signature file found")
#                 flowable_form_builder.build_form(form_to_save=form_to_save, filename=filename,
#                                                  signature_file_path=signature_file_path)

#         return redirect('/view_psych_forms')

# def get_pdf_page(request, pk=None):
#     """
#     Get PDF of a given NormForm via pk id
#     """
#     if request.user.groups.filter(name='Admins').exists() and pk:
#         norm_form = NormForm.objects.get(id=pk)
#         if norm_form.filename:
#             if request.user.email == settings.EMAIL_TO:
#                 if not norm_form.bal_accessed:
#                     norm_form.bal_accessed = datetime.datetime.now()
#                     norm_form.save()
#             # return file from patient_files as pdf response
#             return FileResponse(open(os.path.abspath(os.path.dirname(__file__)) +
#                                      '/patient_files/' +
#                                      norm_form.filename, 'rb'), content_type='application/pdf')
#     return redirect('/')


# def get_preview_pdf_page(request, pk=None):
#     """
#     Create and return Sample PDF based on current form
#     """
#     if request.user.groups.filter(name='Admins').exists() and pk:
#         norm_form = NormForm.objects.get(id=pk)
#         if norm_form.filename:
#             # return file from patient_files as pdf response
#             return FileResponse(open(os.path.abspath(os.path.dirname(__file__)) +
#                                      '/patient_files/' +
#                                      norm_form.filename, 'rb'), content_type='application/pdf')
#     return redirect('/')


# def get_subjective_boilerplate_option_text(request):
#     """
#     Get value of a given SubjectiveBoilerplateOption via $.AJAX in main_card
#     """
#     if not request.user.groups.filter(name='Admins').exists():
#         return redirect('/')
#     if 'ids' in request.GET and request.GET.get('ids'):
#         ids = request.GET.get('ids').split(',')
#     else:
#         return JsonResponse('', safe=False)
#     if request.is_ajax():
#         subjective_boilerplate_options = SubjectiveBoilerplateOption.objects.filter(id__in=ids)
#         response_text = ''
#         for subjective_boilerplate_option in subjective_boilerplate_options:
#             if subjective_boilerplate_option.full_text:
#                 response_text += subjective_boilerplate_option.full_text + ' '
#         return JsonResponse(response_text, safe=False)
#     return redirect('/')


# def get_subjective_option_text(request):
#     """
#     Get value of a given SubjectiveOption via $.AJAX in main_card
#     """
#     if not request.user.groups.filter(name='Admins').exists():
#         return redirect('/')
#     if 'ids' in request.GET and request.GET.get('ids'):
#         ids = request.GET.get('ids').split(',')
#     else:
#         return JsonResponse('', safe=False)
#     if request.is_ajax():
#         subjective_options = SubjectiveOption.objects.filter(id__in=ids)
#         response_text = ''
#         for subjective_option in subjective_options:
#             if subjective_option.full_text:
#                 response_text += subjective_option.full_text + ' '
#         return JsonResponse(response_text, safe=False)
#     return redirect('/')


# def get_discussion_treatment_option_text(request):
#     """
#     Get value of a given DiscussionTreatmentOption via $.AJAX() in main_card
#     """
#     if not request.user.groups.filter(name='Admins').exists():
#         return redirect('/')
#     if 'ids' not in request.GET or request.GET.get('ids'):
#         ids = request.GET.get('ids').split(',')
#     else:
#         return JsonResponse('', safe=False)
#     if request.is_ajax():
#         discussion_treatment_options = DiscussionTreatmentOption.objects.filter(id__in=ids)
#         response_text = ''
#         for discussion_treatment_option in discussion_treatment_options:
#             if discussion_treatment_option.full_text:
#                 response_text += discussion_treatment_option.full_text + ' '
#         return JsonResponse(response_text, safe=False)
#     return redirect('/')


# def get_icd_10_code_text(request):
#     """
#     Get value of a given ICD-10 Code via $.AJAX in main_card
#     """
#     if not request.user.groups.filter(name='Admins').exists():
#         return redirect('/')
#     if 'ids' in request.GET and request.GET.get('ids'):
#         ids = request.GET.get('ids').split(',')
#     else:
#         return JsonResponse('', safe=False)
#     if request.is_ajax():
#         icd_10_codes = Icd10Codes.objects\
#                                  .filter(full_code__startswith="F")\
#                                  .filter(id__in=ids)
#         response_text = ''
#         for icd_10_code in icd_10_codes:
#             if icd_10_code.abbreviated_description:
#                 response_text += icd_10_code.diagnosis_code + ': ' + icd_10_code.abbreviated_description + ' '
#         return JsonResponse(response_text, safe=False)
#     return redirect('/')


# def get_filtered_icd_10_code_text(request):
#     """
#     Given text, filter ICO-10 code choices (return array) via $.AJAX in main_card
#     """
#     if not request.user.groups.filter(name='Admins').exists():
#         return redirect('/')
#     if 'data' in request.GET:
#         filter_text = request.GET.get('data')
#     else:
#         return JsonResponse('', safe=False)
#     if request.is_ajax():
#         if request.GET.get('data') is not None:
#             icd_10_codes = Icd10Codes.objects\
#                                      .filter(full_code__startswith="F")\
#                                      .filter(Q(full_description__icontains=filter_text) |
#                                              Q(diagnosis_code__icontains=filter_text))\
#                                      .values('id', 'diagnosis_code',
#                                              'full_code', 'abbreviated_description',
#                                              'full_description')\
#                                      .order_by('abbreviated_description')\
#                                      .order_by('diagnosis_code')
#         else:
#             icd_10_codes = Icd10Codes.objects\
#                                      .filter(full_code__startswith="F")\
#                                      .values('id', 'diagnosis_code',
#                                              'full_code', 'abbreviated_description',
#                                              'full_description')\
#                                      .order_by('abbreviated_description')\
#                                      .order_by('diagnosis_code')
#         # print(icd_10_codes)
#         return JsonResponse(list(icd_10_codes), safe=False)
#     return redirect('/')

# def email_bal(request, pk=None):
#     """
#     Send Email to Bal with current NormForm
#     """
#     if request.user.groups.filter(name='Admins').exists() and pk:
#         norm_form = NormForm.objects.get(id=pk)
#         if norm_form.filename:
#             # Email Bal
#             send_mail(
#                 'New Form for Norm Hendricksen',
#                 f'Hello Bal!\n\n'
#                 f'There is a new form to process on the MeritBridge Replacement App website\n\n'
#                 f'Please log in at https://form.hendricksenphd.com\n\n'
#                 f'Then, click the link below to see the PDF\n\n'
#                 f'https://form.hendricksenphd.com/get_pdf/{pk}\n\n'
#                 f'Thanks!',
#                 settings.EMAIL_HOST_USER,
#                 [settings.EMAIL_TO],
#                 fail_silently=False,
#             )
#         messages.add_message(request, messages.SUCCESS, "Successfully emailed Bal.")
#         norm_form.emailed = True
#         norm_form.save()
#     return redirect('/view_psych_forms')
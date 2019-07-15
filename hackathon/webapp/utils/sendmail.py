from django.template import loader

html_message = loader.render_to_string(
            'path/to/your/htm_file.html',
            {
                'user_name': user.name,
                'subject':  'Thank you from' + dynymic_data,
                //...
            }
        )
send_mail(subject,message,from_email,to_list,fail_silently=True,html_message=html_message)
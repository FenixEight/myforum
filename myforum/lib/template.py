from mako import exceptions
from flask_mako import render_template


#http://stackoverflow.com/questions/390409/how-do-you-debug-mako-templates
def render(template_name, **context):
	try:
		return render_template(template_name + '.html', **context)
	except:
		return exceptions.html_error_template().render()


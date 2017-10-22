# coding: utf-8
from SisApp import app, db, models
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView


admin = Admin(app, name='SisCond', template_mode='bootstrap3')
admin.add_view(ModelView(models.Condominio, db.session))
admin.add_view(ModelView(models.Apartamento, db.session))
admin.add_view(ModelView(models.Morador, db.session))
admin.add_view(ModelView(models.Servico, db.session))
admin.add_view(ModelView(models.Usuario, db.session))
admin.add_view(ModelView(models.Contato, db.session))

if __name__ == '__main__':
    app.run()

from app import app, db, dao, utils
from flask_admin import Admin, BaseView, expose, AdminIndexView
from app.models import Sach, TheLoai, NhaXuatBan, TacGia, VaiTro
from flask_admin.contrib.sqla import ModelView
from sqlalchemy.orm import relationship
from flask_login import current_user, logout_user
from flask import redirect


class MyAdminIndex(AdminIndexView):
    @expose('/')
    def index(self):
        return self.render('admin/index.html', stats=utils.view_sach())


admin = Admin(app=app, name="Bookshop Administrator", template_mode='bootstrap4', index_view=MyAdminIndex())


class StatsView(BaseView):
    @expose('/')
    def index(self):
        return self.render('admin/stats.html')

    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.__eq__(VaiTro.QL)


class AuthenticatedModelView(ModelView):
    def is_accessible(self):
        return current_user.is_authenticated and current_user.role.__eq__(VaiTro.QL)


class SachView(AuthenticatedModelView):
    column_list = ('id', 'name', 'price', 'image', 'miniid', 'sach_info','quanti' , 'nxb_id')
    can_export = True
    column_filters = ['price', 'name']
    can_view_details = True


class LogoutView(BaseView):
    @expose('/')
    def index(self):
        logout_user()
        return redirect('/admin')

    def is_accessible(self):
        return current_user.is_authenticated


admin.add_view(AuthenticatedModelView(Sach, db.session))
admin.add_view(AuthenticatedModelView(TheLoai, db.session))
admin.add_view(AuthenticatedModelView(NhaXuatBan, db.session))
admin.add_view(AuthenticatedModelView(TacGia, db.session))
admin.add_view(LogoutView(name='Logout'))
admin.add_view(StatsView(name='Stats'))

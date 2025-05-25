from flask import render_template, request, redirect, url_for, flash

class AdminController:
    def show_dashboard(self):

        return render_template('admin/dashboard.html')
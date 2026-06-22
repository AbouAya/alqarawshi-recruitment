from flask import Blueprint, render_template

contact_bp = Blueprint("contact", __name__)


@contact_bp.route('/contact', methods=['GET', 'POST'])
def contact():
    if request.method == 'POST':
        new_message = ContactMessage(
            name=request.form['name'],
            email=request.form['email'],
            phone=request.form['phone'],
            subject=request.form['subject'],
            message=request.form['message']
        )

        db.session.add(new_message)
        db.session.commit()
        msg = Message(
            subject=f"New Contact Message: {request.form['subject']}",
            sender=app.config['MAIL_USERNAME'],
            recipients=['hr@alkarawchi.com']
        )

        msg.body = f"""
        Name: {request.form['name']}
        Email: {request.form['email']}
        Phone: {request.form['phone']}

        Message:

        {request.form['message']}
        """

        mail.send(msg)
        flash('Message sent successfully!')
        return redirect(url_for('contact'))

    return render_template('contact.html')
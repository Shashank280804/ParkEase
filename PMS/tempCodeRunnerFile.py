 LicensePlate(db.Model):
    __tablename__ ='licensceplate'
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(20), nullable=False)
    time = db.Column(db.String(20), nullable=False)
    state = db.Column(db.String(20))
    number = db.Column(db.String(20), nullable=False)
    vehicle_id = db.Column(db.Integer, db.ForeignKey('vehicles.rfid_no'))
    vehicle = relationship('Vehicle', back_populates='plates')

# ... (existing code)

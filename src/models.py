class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, index=True, nullable=False)
    name = Column(String, default="", nullable=False)
    company = Column(String, default="", nullable=False)
    approved = Column(Boolean, default=False, nullable=False)
    eligible = Column(Boolean, default=False, nullable=False)
    contacted = Column(Boolean, default=False, nullable=False)
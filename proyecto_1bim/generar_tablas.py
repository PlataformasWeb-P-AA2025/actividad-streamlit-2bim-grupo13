from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy import Column, Integer, String, ForeignKey

# Importamos el enlace a la base de datos desde el archivo configuracion
from configuracion import cadena_base_datos

# Generamos el enlace al gestor de base de datos
engine = create_engine(cadena_base_datos)
	
Base = declarative_base()

# CREACIÓN DE LAS CLASES NECESARIAS PARA FutRedX
class Usuario(Base):
    __tablename__ = 'usuario'
    id = Column(Integer, primary_key=True)
    nombre = Column(String(100))

    publicaciones = relationship("Publicacion", back_populates="usuario")
    reacciones = relationship("Reaccion", back_populates="usuario")

    def __repr__(self):
        return "Usuario: nombre=%s"% (
                          self.nombre)

class Publicacion(Base):
    __tablename__ = 'publicacion'
    id = Column(Integer, primary_key=True)
    id_usuario = Column(Integer, ForeignKey('usuario.id'))
    publicacion = Column(String(150))

    usuario = relationship("Usuario", back_populates="publicaciones")
    reacciones = relationship("Reaccion", back_populates="publicacion")
    
    def __repr__(self):
        return "Publicación: publicacion=%s"% (
                          self.publicacion)

class Reaccion(Base):
    __tablename__ = 'reaccion'
    id_usuario = Column(Integer, ForeignKey('usuario.id'), primary_key=True)
    id_publicacion = Column(Integer, ForeignKey('publicacion.id'), primary_key=True)
    tipo_emocion = Column(String(25))

    usuario = relationship("Usuario", back_populates="reacciones")
    publicacion = relationship("Publicacion", back_populates="reacciones")

    def __repr__(self):
        return "Reaccion: tipo de emoción=%s"% (
                          self.tipo_emocion)

Base.metadata.create_all(engine)

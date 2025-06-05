import streamlit as st
from db import get_session

# Importa las clases que definiste en clases.py
from generar_tablas import Usuario, Publicacion, Reaccion


st.set_page_config(page_title="Explorador de objetos SQLAlchemy - Proyecto Final 1er Bimestre", layout="wide")

def listar_usuarios():
    """
    Se muestra todos los usuarios y un expander con sus publicaciones y las reacciones que ha hecho.
    """
    st.header("Usuarios")
    session = get_session()
    usuarios = session.query(Usuario).all()


    if not usuarios:
        st.info("No hay registros en 'usuario'.")
        session.close()
        return

    # Para cada Usuario, mostramos un expander que contiene una lista de publicaciones
    for u in usuarios:
        with st.expander(f"ID {u.id} → {u.nombre}", expanded=False):
            # Mostrar atributos básicos
            st.write(f"**ID:** {u.id}")
            st.write(f"**Nombre:** {u.nombre}")

            # Si el usuario tiene publicaciones relacionadas, se las lista
            if u.publicaciones:
                st.write("**Publicaciones hechas:**")
                # Usamos st.table para mostrar el id, el contenido y el número de reacciones
                filas = []
                for p in u.publicaciones:
                    filas.append({
                        "Publicación": p.id,
                        "Contenido": p.publicacion,
                        "Número de Reacciones": len(p.reacciones)
                    })
                st.table(filas)
            else:
                st.write("_Este usuario no ha hecho ninguna publicación._")
    session.close()

def listar_publicaciones():
    """
    Muestra todas las publicaciones y, dentro de cada expander, los usuarios y la reacción que hicieron a la publicación.
    """
    st.header("Publicaciones")
    session = get_session()
    publicaciones = session.query(Publicacion).all()


    if not publicaciones:
        st.info("No hay registros en 'publicacion'.")
        session.close()
        return

    for p in publicaciones:
        with st.expander(f"ID {p.id} → {p.publicacion}", expanded=False):
            st.write(f"**ID:** {p.id}")
            st.write(f"**Contenido:** {p.publicacion}")

            if p.reacciones:
                st.write("**Reacciones obtenidas:**")
                filas = []
                for c in p.reacciones:
                    filas.append({
                        "Usuario": c.usuario.nombre,
                        "Tipo de Emoción": c.tipo_emocion
                    })
                st.table(filas)
            else:
                st.write("_Esta publicación no tiene ninguna reacción._")
    session.close()

def listar_reacciones():
    """
    Muestra todas las reacciones y, para cada una, muestra que usaurio la realizó, y en que publicación fue.
    """
    st.header("Reacciones")
    session = get_session()
    reacciones = session.query(Reaccion).all()

    if not reacciones:
        st.info("No hay registros en 'curso'.")
        session.close()
        return

    for r in reacciones:
        with st.expander(f"Usuario ID {r.id_usuario} → {r.tipo_emocion} → Publicación ID {r.id_publicacion}", expanded=False):
            usuario = r.publicacion.publicacion
            publicacion = r.usuario.nombre
            st.write(f"**Reacción:** {r.tipo_emocion}")
            st.write(f"**Usuario que Reaccionó:** {usuario}")
            st.write(f"**Publicación que Reacionó:** {publicacion}")

    session.close()

def main():
    st.title("Explorador de entidades de FutRedX")

    entidad = st.sidebar.selectbox(
        "Elija la entidad que desea explorar:",
        (
            "Usuario",
            "Publicación",
            "Reación"
        ),
    )

    if entidad == "Usuario":
        listar_usuarios()
    elif entidad == "Publicación":
        listar_publicaciones()
    elif entidad == "Reación":
        listar_reacciones()

if __name__ == "__main__":
    main()

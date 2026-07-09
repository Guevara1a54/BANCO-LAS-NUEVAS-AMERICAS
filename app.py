import streamlit as st
import base64
import os
import pandas as pd
from datetime import datetime
# IMPORTS DE TODOS LOS CONTROLADORES DE TU PROYECTO BANCO
# ==============================================================================
from controladores.sucursal_controlador import SucursalControlador
from controladores.cliente_controlador import ClienteControlador
from controladores.empleado_controlador import EmpleadoControlador
from controladores.cuenta_controlador import CuentaControlador
from controladores.transaccion_controlador import TransaccionControlador
from controladores.guardian_fraudes import FiltroAntifraude  
from dao.cuenta_bancaria_dao import CuentaBancariaDAO
from controladores.tarjeta_controlador import TarjetaControlador
from controladores.prestamo_controlador import PrestamoControlador
from controladores.beneficiario_controlador import BeneficiarioControlador




st.set_page_config(page_title="Banco Las Nuevas Americas", layout="wide")


# FONDO DE RECUADROS PARA TEXTO
def aplicar_diseno_bancario(ruta_logo):
    encoded_string = ""
    if os.path.exists(ruta_logo):
        with open(ruta_logo, "rb") as image_file:
            encoded_string = base64.b64encode(image_file.read()).decode()

    st.markdown(f"""
        <style>
        @import url('https://fonts.cdnfonts.com/css/helvetica-neue-9');
        
        /* 1. FONDO GLOBAL: Abarca absolutamente toda la interfaz */
        .stApp {{
            background-image: linear-gradient(rgba(10, 25, 47, 0.75), rgba(10, 25, 47, 0.85)), 
                              url("data:image/png;base64,{encoded_string}");
            background-attachment: fixed;
            background-size: 85vw !important: contain !important; /*  
            background-position: center center !important; /* Ajustado ligeramente hacia arriba */
            background-repeat: no-repeat !important;
            font-family: 'Helvetica Neue', Helvetica, Arial, sans-serif !important;
            background-color: #0a192f !important; /* No salen parches grises al reproducir la página */
        }}

        /* 2. CONTENEDORES TRANSPARENTES: 
        [data-testid="stHeader"], [data-testid="stVerticalBlock"], .main .block-container {{
            background-color: transparent !important;
        }}       

            /* 3. TÍTULO RESALTADO */        
        .titulo-banco {{
            font-family: 'Helvetica', sans-serif !important;
            font-size: 80px !important;
            font-weight: 900 !important;
            color: #FFFFFF !important; /* Blanco Puro */
            text-align: center !important;
            margin-bottom: 0px !important;
            padding-bottom: 0px !important;
            /* Triple capa de sombra para que el texto resalte de forma impresionante sobre el loro de fondo*/
            text-shadow: 3px 3px 6px rgba(0,0,0,0.9), -2px -2px 4px rgba(0,0,0,0.8), 0 0 20px rgba(0,0,0,0.6) !important;
            letter-spacing: 2px;
        }}

        .lema-banco {{
            font-size: 26px !important;
            color: #D4AF37 !important; /* Dorado */
            text-align: center !important;
            margin-top: 5px !important;
            margin-bottom: 35px !important;
            font-style: italic !important;
            font-weight: 600 !important;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.9) !important;
        }}

        /* 4. RECUADROS DE TEXTO COMBINADOS CON EL FONDO */
        .recuadro-texto {{
            background-color: rgba(17, 34, 64, 0.85) !important; /* Azul oscuro a tono con el fondo */
            border: 2px solid #D4AF37 !important; /* Borde dorado elegante */
            padding: 22px !important;
            border-radius: 12px !important;
            color: #FFFFFF !important;
            text-align: center !important;
            margin: 20px 0px !important;
            box-shadow: 0px 6px 15px rgba(0,0,0,0.6) !important;
        }}

        .texto-presentacion {{ 
            font-size: 22px !important; /* Tamaño mediano */
            line-height: 1.6 !important; 
        }}
        
        .texto-regular {{ 
            font-size: 18px !important; /* Regular: ni pequeño ni mediano */
        }}

        /* 5. MENÚ LATERAL (SIDEBAR) ELEGANTE */
        [data-testid="stSidebar"] {{
            background-color: #050C16 !important;
            border-right: 2px solid #D4AF37 !important;
        }}

        /* PARA CONTENER IMAGENES DENTRO DE CÍRCULOS (Útil en empleados y clientes)
        /* Container applies circle shape, masking, and border 
        .circle-image-container {{
            width: 80px; /* 
            height: 80px; /* Borde dorado elegante */
            margin: 0 auto;
            border-radius: 50%;
            overflow: hidden;
            border: 3px solid #D4AF37;
            display: flex;                  
            justify-content: center;                
            align-items: center;            
            box-shadow: 0px 4px 10px rgba(0,0,0,0.5);
        }}

        /* Las imágenes generadas vayan en el circulo
        .circle-image-container img {{
            width: 100% !important; /* Scale to fill container width */
            height: 100% !important; /* Scale to fill container height */
            object-fit: cover !important; /* Crop without distorting */
            border-radius: 50%; /* Re-apply border radius for masking */
        }}        

        /* Container applies circle shape, masking, and border 
        [data-testid="column"] div.stImage{{
            text-align: center;
        }}    

        </style>
        """, unsafe_allow_html=True)

# 3. EJECUCIÓN GLOBAL DEL DISEÑO 
# Al ponerlo aquí, garantizamos que el CSS se inyecte SIEMPRE, sin importar la opción elegida
aplicar_diseno_bancario("imagenes/lorito_de_fondo.png")

# ==============================================================================
# MENÚ DESPLEGABLE (SIDEBAR) CON SECCIÓN DE CONTACTO FINAL
# ==============================================================================
with st.sidebar:
            # --- PARTE SUPERIOR: Imagen Mediana ---
            try:
                st.image("imagenes/banco.png", use_container_width=True)
            except:
                pass 
            
            st.markdown("<h2 style='color:#D4AF37; text-align:center; margin-top:10px;'>Menú Principal</h2>", unsafe_allow_html=True)
            
            # Menú Principal de Clases/Módulos
            opcion_principal = st.selectbox(
                "Gestión de Módulos:",
                [
                    "Inicio", 
                    "Gestión de Sucursales", 
                    "Gestión de Empleados", 
                    "Gestión de Clientes", 
                    "Cuentas Bancarias y Operaciones", 
                    "Gestión de Préstamos", 
                    "Agenda de Beneficiarios", 
                    "Gestión de Tarjetas (Débito/Crédito)"
                ]
            )

            submenu = None           
        # Submenú Dinámico (Cambia automáticamente según el módulo seleccionado)
            if opcion_principal == "Inicio":
                st.sidebar.info("Bienvenido al Core Bancario. Seleccione un módulo arriba para desplegar operaciones.")  
                st.write("---")
            col1, col2, col3 = st.columns(3)
                
            with col1:
                st.markdown("""
                        <div style="background-color:#1E293B; padding:12px; border-radius:8px; text-align:center; border: 1px solid #2D3748;">
                            <p style="color:#A0AEC0; font-size:12px; margin:0; text-transform:uppercase; letter-spacing:1px;">Estado del Sistema</p>
                            <h4 style="color:#00FF00; margin:5px 0 2px 0; font-size:18px;">🟢 ONLINE</h4>
                            <p style="color:#718096; font-size:11px; margin:0;">Canal Seguro</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
            with col2:
                st.markdown("""
                        <div style="background-color:#1E293B; padding:12px; border-radius:8px; text-align:center; border: 1px solid #2D3748;">
                            <p style="color:#A0AEC0; font-size:12px; margin:0; text-transform:uppercase; letter-spacing:1px;">Motor Antifraude</p>
                            <h4 style="color:#3182CE; margin:5px 0 2px 0; font-size:18px;">🧠 ACTIVO</h4>
                            <p style="color:#718096; font-size:11px; margin:0;">Paquito Random Forest Classifier</p>
                        </div>
                    """, unsafe_allow_html=True)
                    
            with col3:
                st.markdown("""
                        <div style="background-color:#1E293B; padding:12px; border-radius:8px; text-align:center; border: 1px solid #2D3748;">
                            <p style="color:#A0AEC0; font-size:12px; margin:0; text-transform:uppercase; letter-spacing:1px;">Base de Datos</p>
                            <h4 style="color:#E2E8F0; margin:5px 0 2px 0; font-size:18px;">🗄️ CONECTADO</h4>
                            <p style="color:#718096; font-size:11px; margin:0;">MySQL Server</p>
                        </div>
                    """, unsafe_allow_html=True)
        
            st.write("---")

            if "Sucursales" in opcion_principal:                    
                opciones_submenu = [
                        "Registrar sucursal.",
                        "Listar sucursales.",
                        "Buscar sucursal por ID.",
                        "Modificar sucursal.",
                        "Eliminar sucursal.",
                        "Ver empleados de una sucursal." 
                    ]
                submenu = st.sidebar.radio("Seleccione una opción:", opciones_submenu)
            elif "Empleados" in opcion_principal:
                opciones_submenu = [
                        "Registrar empleado.",
                        "Listar empleados.",
                        "Buscar empleado por ID.",
                        "Modificar empleado.",
                        "Eliminar empleado."
                    ]
                submenu = st.sidebar.radio("Seleccione una opción:", opciones_submenu)
            elif "Clientes" in opcion_principal:
                opciones_submenu = [
                        "Registrar cliente.",
                        "Listar clientes.",
                        "Buscar cliente por ID.",
                        "Modificar cliente.",
                        "Eliminar cliente.",
                        "Ver cuentas bancarias de un cliente." 
                ]    
                submenu = st.sidebar.radio("Seleccione una opción:", opciones_submenu)

            elif "Cuentas Bancarias" in opcion_principal:                
                opciones_submenu = [
                    "Abrir cuenta bancaria.",
                        "Listar todas las cuentas.",
                        "Consultar cuenta por ID (Ver saldo).",
                        "Realizar Depósito.",
                        "Realizar Retiro.",
                        "Realizar Transferencia.",
                        "Ver historial de transacciones de la cuenta...",
                        "Cancelar/Eliminar cuenta."
                ]
                submenu = st.sidebar.radio("Seleccione una opción:", opciones_submenu)

            elif "Préstamos" in opcion_principal:                
                opciones_submenu = [
                        "Solicitar/Registrar préstamo.",
                        "Listar todos los préstamos.",
                        "Buscar préstamo por ID.",
                        "Cambiar estado de préstamo (Aprobar/Liquidar).",
                        "Eliminar registro de préstamo.",
                ]
                submenu = st.sidebar.radio("Seleccione una opción:", opciones_submenu)

            elif "Beneficiarios" in opcion_principal:
                opciones_submenu = [
                    "Agregar beneficiario frecuente.",
                    "Listar mis beneficiarios.",
                    "Buscar beneficiario por ID.",
                    "Modificar datos de beneficiario.",
                    "Eliminar beneficiario de la agenda."
                ]
                submenu = st.sidebar.radio("Seleccione una opción:", opciones_submenu)

            elif "Tarjetas" in opcion_principal:
                opciones_submenu = [
                    "Emitir / Registrar tarjeta.",
                    "Listar todas las tarjetas.",
                    "Consultar tarjeta por ID.",
                    "Modificar datos de tarjeta.",
                    "Bloquear / Eliminar tarjeta."
                ]
                submenu = st.sidebar.radio("Seleccione una opción:", opciones_submenu)
            else:
                st.sidebar.write("Seleccione un módulo válido.")



# ==============================================================================
#                   CONTROL DE FLUJO DE LAS PÁGINAS 
# ==============================================================================

if opcion_principal == "Inicio":
    # --------------------------------------------------------------------------
    # Pagina principal INICIO 
    # --------------------------------------------------------------------------
    
    # 1. TÍTULO PRINCIPAL (Grande y en Helvetica)
    st.markdown('<h1 class="titulo-banco">BANCO</h1>', unsafe_allow_html=True)
    st.markdown('<h1 class="titulo-banco" style="font-size:68px !important; margin-top:-20px !important;">LAS NUEVAS AMÉRICAS</h1>', unsafe_allow_html=True)
    
    # 2. LEMA (Tamaño casi mediano / Dorado)
    st.markdown('<p class="lema-banco">"Seguridad que vuela alto, confianza que permanece."</p>', unsafe_allow_html=True)

    # 3. IMAGEN CENTRAL GRANDE (BANNER DEL EDIFICIO)
    try:
        col_izq, col_centro, col_der = st.columns([12, 76, 12])
        with col_centro:
            st.image("imagenes/banco_fachada.png", use_container_width=True)
    except:
        st.warning("⚠️ No se pudo cargar 'imagenes/banco_fachada.png'")

    # 4. TEXTO DE PRESENTACIÓN EN RECUADRO ELEGANTE (Tamaño Mediano)
    st.markdown("""
        <div class="recuadro-texto texto-presentacion">
            BIENVENIDOS. BIENVENIDOS A BANCO LAS NUEVAS AMERICAS. UNA INSTITUCIÓN FINNACIERA LÍDER EN INNOVACIÓN.
            UN LUGAR SEGURO...
            EN BANCO LAS NUEVAS AMERICAS, NOS ENORGULLECEMOS DE GESTIONAR SU PATRIMONIO CON LA ELEGANCIA EXACTA Y PRECISA
            QUE CADA UNO DE USTEDES SE MERECE. CONECTAMOS SUS SUEÑOS CON SOLUCIONES REALES. 
        </div>
    """, unsafe_allow_html=True)

    st.write("") # Espaciador estético

    # 5. DOS IMÁGENES INFERIORES CON SUS TEXTOS REGULARES RECUADRADOS
    col1, col2 = st.columns(2)
    
    with col1:
        try: 
            st.image("imagenes/recepcion.png", use_container_width=True)
        except: 
            st.error("Falta la imagen: imagenes/recepcion.png")
            
        st.markdown("""
            <div class="recuadro-texto texto-regular">
                <b>Banca Privada</b><br>
                Atención personalizada y exclusiva para grandes inversiones.
            </div>
        """, unsafe_allow_html=True)

    with col2:
        try: 
            st.image("imagenes/asesoria.png", use_container_width=True)
        except: 
            st.error("⚠️ Falta la imagen: imagenes/asesoria.png")
            
        st.markdown("""
            <div class="recuadro-texto texto-regular">
                <b>Préstamos Ágiles</b><br>
                Financiamiento diseñado para el crecimiento de sus proyectos.
            </div>
        """, unsafe_allow_html=True)

    # --- PARTE INFERIOR: SECCIÓN FIJA DE CONTACTO Y CRÉDITOS ---
         # Usamos saltos de línea grandes para empujar esta sección al fondo del menú
    st.markdown("<br><br><br><hr style='border:1px solid rgba(214, 175, 55, 0.3);'>", unsafe_allow_html=True)
            
            # Título de la sección
    st.markdown("<h4 style='color:#D4AF37; text-align:center;'>📞 Contáctenos</h4>", unsafe_allow_html=True)
            
            # Información de Ubicación (Perú y su logo pequeño simulado con emoji o texto)
    st.markdown("""
                <p style='color:#E6E6E6; font-size:14px; margin-bottom:5px; text-align:center;'>
                    🇵🇪 <b>Sede Central:</b> Lima, Perú
                </p>
            """, unsafe_allow_html=True)
            
            # Correo Electrónico Ficticio
    st.markdown("""
                <p style='color:#E6E6E6; font-size:14px; margin-bottom:15px; text-align:center;'>
                    ✉️ <b>Soporte:</b> <a href='mailto:contacto@lasnuevasamericas.com' style='color:#D4AF37; text-decoration:none;'>contacto@lasnuevasamericas.com</a>
                </p>
            """, unsafe_allow_html=True)
            
            # Agradecimientos / Créditos clásicos
    st.markdown("""
                <div style='background-color: rgba(17, 34, 64, 0.5); padding: 10px; border-radius: 5px; border: 1px solid rgba(212, 175, 55, 0.2);'>
                    <p style='color:#A0AEC0; font-size:12px; text-align:center; margin:0;'>
                        <b>Agradecimientos:</b><br>
                        Gracias por confiar en nuestra plataforma de gestión bancaria automatizada. 
                        <br><b>Un lugar seguro...</b>
                    </p>
                </div>
            """, unsafe_allow_html=True)
            
    st.markdown("<br>", unsafe_allow_html=True)
            

# -----------------------------------------------------------------------------------------------------------
# Vamos con el resto de módulos
# SUCURSALES...

elif "Sucursales" in opcion_principal:
    st.markdown("<h1 style='color:#FFFFFF; margin-bottom: 20px;'>🏢 Gestión de Sucursales</h1>", unsafe_allow_html=True)
    
    imagenes_personalizadas = {
        "S0001": "Mall.png", "S0002": "Loreto.jpg", "S0003": "Trujillo.png",
        "S0004": "Lima.png", "S0005": "Sur.jpeg", "S0006": "Cusco.png", "S0007": "Puno.png"
    }

    # --- 1. REGISTRAR SUCURSAL ---
    if submenu == "Registrar sucursal.":
        st.markdown("<h3 style='color:#D4AF37;'>✍️ Registrar Nueva Sucursal:</h3>", unsafe_allow_html=True)
        st.markdown('<div class="recuadro-texto" style="text-align: left !important;">', unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            idSucursal = st.text_input("ID sucursal:", placeholder="Ej. S0008").strip()
            nombre = st.text_input("Nombre:").strip()
            direccion = st.text_input("Dirección:").strip()
        with col_f2:
            telefono = st.text_input("Teléfono:").strip()
            estado = st.selectbox("Estado:", ["Activo", "Remodelacion", "Cerrado"])
            
        if st.button("Registrar sucursal", type="primary"):
            if not idSucursal or not nombre:
                st.error("⚠️ ID y Nombre son obligatorios.")
            else:
                if SucursalControlador.registrar(idSucursal, nombre, direccion, telefono, estado):
                    st.success("Sucursal registrada correctamente.")
                else:
                    st.error("No se pudo registrar la Sucursal.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 2. LISTAR SUCURSALES ---
    elif submenu == "Listar sucursales.":
        st.markdown("<h3 style='color:#D4AF37;'>📋 Sucursales Disponibles:</h3>", unsafe_allow_html=True)
        sucursales = SucursalControlador.listar()
        if not sucursales:
            st.info("No hay sucursales registradas.")
        else:
            sucursales = sorted(sucursales, key=lambda x: x.idSucursal)
            columnas_web = st.columns(2)
            for index, suc in enumerate(sucursales):
                col_actual = columnas_web[index % 2]
                with col_actual:
                    st.markdown(f"""
                        <div class="recuadro-texto" style="margin: 10px 0px; padding: 15px; text-align: left !important;">
                            <b style="font-size: 20px; color: #D4AF37;">🏢 {suc.nombre}</b><br>
                            <span style="color: #A0AEC0; font-size: 14px;">Código: {suc.idSucursal}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    nombre_archivo = imagenes_personalizadas.get(suc.idSucursal, f"{suc.idSucursal}.jpg")
                    try: st.image(f"imagenes/{nombre_archivo}", use_container_width=True)
                    except: st.caption("📷 Imagen no disponible")
                    
                    with st.expander(f"🔍 Ver datos de {suc.nombre}"):
                        st.write(f"**📍 Dirección:** {suc.direccion}")
                        st.write(f"**📞 Teléfono:** {suc.telefono}")
                        st.write(f"**🟢 Estado:** {suc.estado}")
                    st.write("---")

    # --- 3. BUSCAR SUCURSAL POR ID ---
    elif submenu == "Buscar sucursal por ID.":
        st.markdown("<h3 style='color:#D4AF37;'>🔍 Buscar Sucursal por ID:</h3>", unsafe_allow_html=True)
        id_buscar = st.text_input("ID sucursal:").strip()
        if id_buscar:
            sucursal = SucursalControlador.buscar(id_buscar)
            if sucursal is None:
                st.error("Sucursal no encontrada.")
            else:
                st.markdown('<div class="recuadro-texto" style="text-align: left !important;">', unsafe_allow_html=True)
                col_img, col_info = st.columns([40, 60])
                with col_img:
                    nombre_archivo = imagenes_personalizadas.get(sucursal.idSucursal, f"{sucursal.idSucursal}.jpg")
                    try: st.image(f"imagenes/{nombre_archivo}", use_container_width=True)
                    except: st.caption("📷 Imagen no disponible")
                with col_info:
                    st.markdown(f"<h4>🏢 Sede: {sucursal.nombre}</h4>", unsafe_allow_html=True)
                    st.write(f"**ID:** {sucursal.idSucursal}")
                    st.write(f"**Dirección:** {sucursal.direccion}")
                    st.write(f"**Teléfono:** {sucursal.telefono}")
                    st.write(f"**Estado:** {sucursal.estado}")
                st.markdown('</div>', unsafe_allow_html=True)

    # --- 4. MODIFICAR SUCURSAL ---
    elif submenu == "Modificar sucursal.":
        st.markdown("<h3 style='color:#D4AF37;'>🔄 Modificar Sucursal:</h3>", unsafe_allow_html=True)
        id_modificar = st.text_input("ID sucursal a modificar:").strip()
        if id_modificar:
            sucursal = SucursalControlador.buscar(id_modificar)
            if sucursal is None:
                st.error("Sucursal no encontrada.")
            else:
                st.markdown('<div class="recuadro-texto" style="text-align: left !important;">', unsafe_allow_html=True)
                estados_lista = ["Activo", "Remodelacion", "Cerrado"]
                index_estado = estados_lista.index(sucursal.estado) if sucursal.estado in estados_lista else 0
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    nuevo_nombre = st.text_input("Nuevo nombre:", value=sucursal.nombre).strip()
                    nueva_direccion = st.text_input("Nueva dirección:", value=sucursal.direccion).strip()
                with col_m2:
                    nuevo_telefono = st.text_input("Nuevo teléfono:", value=sucursal.telefono).strip()
                    nuevo_estado = st.selectbox("Nuevo estado:", estados_lista, index=index_estado)
                
                nueva_foto = st.file_uploader("📸 Reemplazar foto (.jpg)", type=["jpg", "jpeg", "png"])
                
                if st.button("🔄 Modificar sucursal:"):
                    reg_ok = SucursalControlador.modificar(sucursal.idSucursal, nuevo_nombre, nueva_direccion, nuevo_telefono, nuevo_estado)
                    img_ok = False
                    if nueva_foto is not None:
                        try:
                            archivo = imagenes_personalizadas.get(sucursal.idSucursal, f"{sucursal.idSucursal}.jpg")
                            with open(f"imagenes/{archivo}", "wb") as f: f.write(nueva_foto.getbuffer())
                            img_ok = True
                        except: pass
                    if reg_ok or img_ok:
                        st.success("Sucursal modificada correctamente.")
                        st.rerun()
                st.markdown('</div>', unsafe_allow_html=True)

    # --- 5. ELIMINAR SUCURSAL ---
    elif submenu == "Eliminar sucursal.":
        st.markdown("<h3 style='color:#FF4B4B;'>🗑️ Eliminar Sucursal:</h3>", unsafe_allow_html=True)
        id_eliminar = st.text_input("ID sucursal a eliminar:").strip()
        if id_eliminar:
            sucursal = SucursalControlador.buscar(id_eliminar)
            if sucursal is None:
                st.error("Sucursal no encontrada.")
            else:
                st.markdown('<div class="recuadro-texto" style="border: 2px solid #FF4B4B !important; text-align: left !important;">', unsafe_allow_html=True)
                st.write(f"⚠️ **¿Está seguro de eliminar la sucursal {sucursal.nombre}?**")
                confirmar = st.checkbox("Confirmo la eliminación permanente.")
                if st.button("❌ Eliminar sucursal"):
                    if confirmar:
                        if SucursalControlador.eliminar(id_eliminar):
                            st.success("Sucursal eliminada correctamente.")
                        else:
                            st.error("No se pudo eliminar la sucursal.")
                st.markdown('</div>', unsafe_allow_html=True)

    # --- 6. VER EMPLEADOS DE UNA SUCURSAL ---
    elif submenu == "Ver empleados de una sucursal.":
        st.markdown("<h3 style='color:#D4AF37;'>👥 Empleados por Sucursal</h3>", unsafe_allow_html=True)
        st.write("Listado del personal asignado y estado financiero de la sucursal seleccionada.")
        
        id_suc_buscar = st.text_input("Ingrese el Código de la Sucursal (Ej: S0001, S0003, S0005):").strip()
        
        if id_suc_buscar:
            from controladores.sucursal_controlador import SucursalControlador
            import pandas as pd
            
            # Recuperamos los objetos desde tu controlador
            empleados_data = SucursalControlador.listar_empleados_sucursal(id_suc_buscar)
            
            if not empleados_data:
                st.info(f"No se encontraron empleados registrados en la sucursal '{id_suc_buscar}' o el código no existe.")
            else:
                try:
                    # 1. Convertimos los objetos a una lista limpia de diccionarios
                    lista_limpia_dicts = []
                    for emp in empleados_data:
                        nom = getattr(emp, "nombres", "")
                        ape = getattr(emp, "apellidos", "")
                        
                        lista_limpia_dicts.append({
                            "ID Empleado": getattr(emp, "idEmpleado", "N/A"),
                            "Nombre Completo": f"{nom} {ape}".strip(),
                            "Cargo / Puesto": getattr(emp, "cargo", "Asesor"),
                            "Sueldo Base (S/.)": float(getattr(emp, "salario", 0.0))
                        })
                    
                    # 2. Creamos el DataFrame final listo
                    df_final = pd.DataFrame(lista_limpia_dicts)
                    
                    # 3. 🚀 MUESTRA LA TABLA CON EL COMPONENTE INMUNE DE STREAMLIT
                    # Esto dibuja una tabla interactiva perfecta, limpia y sin bugs de HTML
                    st.dataframe(
                        df_final, 
                        use_container_width=True, 
                        hide_index=True
                    )
                    
                except Exception as e:
                    st.error(f"Error al procesar el listado de personal: {e}")

# -----------------------------------------------------------------------------------------------------------
# Vamos 
# EMPLEADOS...
elif "Empleados" in opcion_principal:
    st.markdown("<h1 style='color:#FFFFFF; margin-bottom: 20px;'> Gestión de Empleados</h1>", unsafe_allow_html=True)

    # --- 1. REGISTRAR EMPLEADOS ---
    if submenu == "Registrar empleado.":
        st.markdown("<h3 style='color:#D4AF37;'>✍️ Registrar Empleado:</h3>", unsafe_allow_html=True)
        st.markdown('<div class="recuadro-texto" style="text-align: left !important;">', unsafe_allow_html=True)
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            idEmpleado = st.text_input("ID empleado:").strip()
            dni = st.text_input("DNI:").strip()
            nombres = st.text_input("Nombres:").strip()
            apellidos = st.text_input("Apellidos:").strip()
        with col_f2:
            cargo = st.text_input("Cargo:").strip()
            salario = st.number_input("Salario:", min_value=0.0, value=0.0)
            telefono = st.text_input("Teléfono:").strip()
            estado = st.selectbox("Estado (Activo/Inactivo):", ["Activo", "Inactivo"])
            idSucursal = st.text_input("ID Sucursal de trabajo:").strip()
            
        # 📸 Añadimos el componente para subir la foto desde la PC
        foto_nueva = st.file_uploader("Subir foto de perfil del colaborador (.jpg, .png)", type=["jpg", "jpeg", "png"])
            
        if st.button("💾 Registrar empleado", type="primary"):
            if not idEmpleado or not nombres or not idSucursal:
                st.error("⚠️ Los campos ID Empleado, Nombres e ID Sucursal son completamente obligatorios.")
            else:
                if EmpleadoControlador.registrar(idEmpleado, dni, nombres, apellidos, cargo, salario, telefono, estado, idSucursal):                    
                    if foto_nueva is not None:
                        try:
                            import os
                            os.makedirs("imagenes/empleados", exist_ok=True)
                            
                            with open(f"imagenes/empleados/{idEmpleado}.jpg", "wb") as f:
                                f.write(foto_nueva.getbuffer())
                            st.success("Empleado registrado y foto guardada correctamente.")
                        except Exception as e:
                            st.warning(f"⚠️ El empleado se registró en MySQL, pero hubo un detalle al guardar el archivo: {e}")
                    else:
                        st.success("Empleado registrado correctamente (sin foto de perfil).")
                else:
                    st.error("❌ No se pudo registrar el empleado. Verifique si el ID ya existe o si la Sucursal es correcta.")
        st.markdown('</div>', unsafe_allow_html=True)

# --- 2. LISTAR EMPLEADOS ---
    elif submenu == "Listar empleados.":
        st.markdown("<h3 style='color:#D4AF37;'>📋 Lista de Empleados:</h3>", unsafe_allow_html=True)

# INYECCIÓN DE CSS EXCLUSIVA PARA ESTE LISTADO
        st.markdown("""
            <style>
                /* Buscamos la imagen nativa que genera Streamlit dentro de esta sección */
                div[data-testid="stImage"] img {
                    width: 80px !important;
                    height: 80px !important;
                    object-fit: cover !important;
                    border-radius: 50% !important;
                    border: 3px solid #D4AF37 !important;
                    display: block;
                    margin: 0 auto;
                }
                /* Centramos el bloque contenedor de la imagen */
                div[data-testid="stImage"] {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
            </style>
        """, unsafe_allow_html=True)

        empleados = EmpleadoControlador.listar()
        
        if not empleados:
            st.info("No hay empleados registrados.")
        else:
            # Ordenamos por ID
            empleados = sorted(empleados, key=lambda x: x.idEmpleado)
            
            # Rejilla de 2 columnas
            columnas_web = st.columns(2)
            
            for index, emp in enumerate(empleados):
                col_actual = columnas_web[index % 2]
                
                with col_actual:
                    st.markdown('<div class="recuadro-texto" style="margin: 10px 0px; padding: 15px; text-align: center !important;">', unsafe_allow_html=True)
                    
                    # Estructura de columnas para centrar la foto
                    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
                    with col_c2:
                        ruta_foto = f"imagenes/empleados/{emp.idEmpleado}.jpg"
                        import os
                        
                        if os.path.exists(ruta_foto):
                            # El CSS inyectado arriba modificará este componente automáticamente
                            st.image(ruta_foto)
                        else:
                            # Silueta por defecto si no tiene archivo asignado
                            st.markdown('<div style="width: 80px; height: 80px; background-color: #2D3748; border: 3px solid #A0AEC0; display: flex; justify-content: center; align-items: center; border-radius: 50%; margin: 0 auto;">👤</div>', unsafe_allow_html=True)
                        
                    st.markdown(f"""
                            <b style="font-size: 18px; color: #D4AF37;">{emp.nombres} {emp.apellidos}</b><br>
                            <span style="color: #FFFFFF; font-size: 14px;"><b>Cargo:</b> {emp.cargo}</span><br>
                            <span style="color: #A0AEC0; font-size: 12px;">ID: {emp.idEmpleado}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Acordeón con detalles adicionales
                    with st.expander(f"🔍 Ver expediente completo:"):
                        st.write(f"**🪪 DNI:** {emp.dni}")
                        st.write(f"**💼 Sede:** {emp.sucursal.nombre}")
                        st.write(f"**💵 Salario:** S/. {emp.salario:.2f}")
                        st.write(f"**📞 Teléfono:** {emp.telefono}")
                        
                        if emp.estado.strip().lower() == "activo":
                            st.markdown("<p style='color:#00FF00; margin:0;'><b>🟢 Estado:</b> Activo</p>", unsafe_allow_html=True)
                        else:
                            st.markdown("<p style='color:#FF0000; margin:0;'><b>🔴 Estado:</b> Inactivo</p>", unsafe_allow_html=True)
                            
                    st.write("---")
                    

    # --- 3. BUSCAR EMPLEADO POR ID ---
    elif submenu == "Buscar empleado por ID.":
        st.markdown("<h3 style='color:#D4AF37;'>🔍 Buscar empleado por ID</h3>", unsafe_allow_html=True)
        id_buscar = st.text_input("ID empleado:").strip()
        if id_buscar:
            empleado = EmpleadoControlador.buscar(id_buscar)
            if empleado is None:
                st.error("Empleado no encontrado.")
            else:
                st.markdown('<div class="recuadro-texto" style="text-align: left !important;">', unsafe_allow_html=True)
                col_img, col_info = st.columns([35, 65])
                with col_img:
                    try: st.image(f"imagenes/empleados/{empleado.idEmpleado}.jpg", use_container_width=True)
                    except: st.caption("📷 Foto no disponible")
                with col_info:
                    st.markdown(f"<h4>📌 {empleado.nombres} {empleado.apellidos}</h4>", unsafe_allow_html=True)
                    st.write(f"**Cargo:** {empleado.cargo}")
                    st.write(f"**Sede:** {empleado.sucursal.nombre}")
                    st.write(f"**Salario:** S/. {empleado.salario:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

    # --- 4. MODIFICAR EMPLEADO ---
    elif submenu == "Modificar empleado.":
        st.markdown("<h3 style='color:#D4AF37;'>🔄 Modificar empleado</h3>", unsafe_allow_html=True)
        id_modificar = st.text_input("ID empleado a modificar:").strip()
        if id_modificar:
            empleado = EmpleadoControlador.buscar(id_modificar)
            if empleado is None:
                st.error("Empleado no encontrado.")
            else:
                st.markdown('<div class="recuadro-texto" style="text-align: left !important;">', unsafe_allow_html=True)
                st.write("Empleado actual:", empleado)
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    dni = st.text_input("Nuevo DNI:", value=empleado.dni).strip()
                    nombres = st.text_input("Nuevos nombres:", value=empleado.nombres).strip()
                    apellidos = st.text_input("Nuevos apellidos:", value=empleado.apellidos).strip()
                    cargo = st.text_input("Nuevo cargo:", value=empleado.cargo).strip()
                with col_m2:
                    salario = st.number_input("Nuevo salario:", min_value=0.0, value=float(empleado.salario))
                    telefono = st.text_input("Nuevo teléfono:", value=empleado.telefono).strip()
                    estado = st.selectbox("Nuevo estado:", ["Activo", "Inactivo"], index=0 if empleado.estado == "Activo" else 1)
                    idSucursal = st.text_input("Nueva ID Sucursal:", value=empleado.sucursal.idSucursal).strip()
                
                # Componente para subir/reemplazar la foto
                nueva_foto = st.file_uploader("📸 Actualizar foto de perfil (.jpg o .png)", type=["jpg", "jpeg", "png"])
                
                if st.button("🔄 Guardar Cambios"):
                    if not nombres or not idSucursal:
                        st.error("⚠️ Los campos Nombres e ID Sucursal no pueden quedar vacíos.")
                    else:
                        # 1. Enviar datos al Controlador respetando el orden estricto de tus parámetros
                        reg_ok = EmpleadoControlador.modificar(
                            id_modificar,  # idEmpleado
                            dni, 
                            nombres, 
                            apellidos, 
                            cargo, 
                            salario, 
                            telefono, 
                            estado, 
                            idSucursal
                        )
                        
                        img_ok = False
                        # 2. Si hay una nueva foto cargada, guardarla en el disco duro
                        if nueva_foto is not None:
                            try:
                                import os
                                # Nos aseguramos que la carpeta exista
                                os.makedirs("imagenes/empleados", exist_ok=True)
                                
                                # Ruta destino fija en minúsculas y extensión .jpg
                                ruta_destino = f"imagenes/empleados/{id_modificar}.jpg"
                                
                                with open(ruta_destino, "wb") as f:
                                    f.write(nueva_foto.getbuffer())
                                img_ok = True
                            except Exception as e:
                                st.error(f"❌ Error al guardar físicamente la foto: {e}")
                        
                        # 3. Evaluar el éxito de las operaciones
                        if reg_ok or img_ok:
                            st.success("✨ ¡Empleado modificado y foto actualizada correctamente!")
                            # Forzamos recarga para que los cambios se reflejen de inmediato al listar
                            st.rerun()
                        else:
                            st.warning("ℹ️ No se detectaron cambios nuevos o la actualización falló en MySQL (verifica si la ID de Sucursal existe).")
                            
                st.markdown('</div>', unsafe_allow_html=True)

    # --- 5. ELIMINAR EMPLEADO ---
    elif submenu == "Eliminar empleado.":
        st.markdown("<h3 style='color:#FF4B4B;'>🗑️ Eliminar empleado</h3>", unsafe_allow_html=True)
        id_eliminar = st.text_input("ID empleado a eliminar:").strip()
        if id_eliminar:
            empleado = EmpleadoControlador.buscar(id_eliminar)
            if empleado is None:
                st.error("Empleado no encontrado.")
            else:
                st.markdown('<div class="recuadro-texto" style="border: 2px solid #FF4B4B !important; text-align: left !important;">', unsafe_allow_html=True)
                confirmacion = st.checkbox("¿Está seguro? (s/n)")
                if st.button("❌ Eliminar empleado"):
                    if confirmacion:
                        if EmpleadoControlador.eliminar(id_eliminar):
                            st.success("Empleado eliminado correctamente.")
                        else:
                            st.error("No se pudo eliminar el empleado.")
                st.markdown('</div>', unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------------------------
# Vamos 
# CLIENTES...

elif "Clientes" in opcion_principal:
    st.markdown("<h1 style='color:#FFFFFF; margin-bottom: 20px;'>👥 Gestión de Clientes</h1>", unsafe_allow_html=True)

    # --- 1. REGISTRAR CLIENTE ---
    if submenu == "Registrar cliente.":
        st.markdown("<h3 style='color:#D4AF37;'>✍️ Registrar Nuevo Cliente:</h3>", unsafe_allow_html=True)
        st.markdown('<div class="recuadro-texto" style="text-align: left !important;">', unsafe_allow_html=True)
        
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            idCliente = st.text_input("ID cliente:", placeholder="Ej. C0001").strip()
            dni = st.text_input("DNI:").strip()
            nombres = st.text_input("Nombres:").strip()
            apellidos = st.text_input("Apellidos:").strip()
            direccion = st.text_input("Dirección:").strip()
        with col_f2:
            telefono = st.text_input("Teléfono:").strip()
            email = st.text_input("Email:").strip()
            estado = st.selectbox("Estado:", ["Activo", "Baneado"])
            idSucursal = st.text_input("ID Sucursal a la que pertenece:").strip()
            
        foto_nueva = st.file_uploader("Subir foto de perfil del cliente (.jpg, .png)", type=["jpg", "jpeg", "png"])
            
        if st.button("💾 Registrar cliente", type="primary"):
            if not idCliente or not nombres or not idSucursal:
                st.error("⚠️ Los campos ID Cliente, Nombres e ID Sucursal son obligatorios.")
            else:
                if ClienteControlador.registrar(idCliente, dni, nombres, apellidos, direccion, telefono, email, estado, idSucursal):
                    if foto_nueva is not None:
                        try:
                            import os
                            os.makedirs("imagenes/clientes", exist_ok=True)
                            with open(f"imagenes/clientes/{idCliente}.jpg", "wb") as f:
                                f.write(foto_nueva.getbuffer())
                            st.success("✨ ¡Cliente registrado y foto guardada correctamente!")
                        except Exception as e:
                            st.warning(f"⚠️ Cliente registrado en la BD, pero hubo un detalle al guardar la foto: {e}")
                    else:
                        st.success("✨ ¡Cliente registrado correctamente (sin foto)!")
                else:
                    st.error("❌ No se pudo registrar el cliente. Verifique si el ID ya existe o si la Sucursal es correcta.")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- 2. LISTAR CLIENTES ---
    elif submenu == "Listar clientes.":
        st.markdown("<h3 style='color:#D4AF37;'>📋 Clientes Registrados:</h3>", unsafe_allow_html=True)

        st.markdown("""
            <style>
                /* Buscamos la imagen nativa que genera Streamlit dentro de esta sección */
                div[data-testid="stImage"] img {
                    width: 80px !important;
                    height: 80px !important;
                    object-fit: cover !important;
                    border-radius: 50% !important;
                    border: 3px solid #D4AF37 !important;
                    display: block;
                    margin: 0 auto;
                }
                /* Centramos el bloque contenedor de la imagen */
                div[data-testid="stImage"] {
                    display: flex;
                    justify-content: center;
                    align-items: center;
                }
            </style>
        """, unsafe_allow_html=True)

        clientes = ClienteControlador.listar()
        
        if not clientes:
            st.info("No hay clientes registrados.")
        else:
            columnas_web = st.columns(2)
            for index, cli in enumerate(clientes):
                col_actual = columnas_web[index % 2]
                with col_actual:
                    st.markdown('<div class="recuadro-texto" style="margin: 10px 0px; padding: 15px; text-align: center !important;">', unsafe_allow_html=True)
                    
                    # Renderizado nativo y centrado de la foto circular
                    col_c1, col_c2, col_c3 = st.columns([1, 2, 1])
                    with col_c2:
                        ruta_foto = f"imagenes/clientes/{cli.idCliente}.jpg"
                        import os
                        if os.path.exists(ruta_foto):
                            st.image(ruta_foto)
                        else:
                            st.markdown('<div style="width: 80px; height: 80px; background-color: #2D3748; border: 3px solid #A0AEC0; display: flex; justify-content: center; align-items: center; border-radius: 50%; margin: 0 auto;">👤</div>', unsafe_allow_html=True)                    
                    st.markdown(f"""
                            <b style="font-size: 18px; color: #D4AF37;">{cli.nombres} {cli.apellidos}</b><br>
                            <span style="color: #FFFFFF; font-size: 14px;">📬 {cli.email}</span><br>
                            <span style="color: #A0AEC0; font-size: 12px;">ID: {cli.idCliente}</span>
                        </div>
                    """, unsafe_allow_html=True)
                    
                    with st.expander(f"🔍 Ver expediente de {cli.nombres}"):
                        st.write(f"**🪪 DNI:** {cli.dni}")
                        st.write(f"**📍 Dirección:** {cli.direccion}")
                        st.write(f"**📞 Teléfono:** {cli.telefono}")
                        st.write(f"**🏢 Sede asignada:** {cli.sucursal.nombre}")
                        if cli.estado.strip().lower() == "activo":
                            st.markdown("<p style='color:#00FF00; margin:0;'><b>🟢 Estado:</b> Activo</p>", unsafe_allow_html=True)
                        else:
                            st.markdown("<p style='color:#FF4B4B; margin:0;'><b>🔴 Estado:</b> Baneado</p>", unsafe_allow_html=True)
                    st.write("---")

    # --- 3. BUSCAR CLIENTE POR ID ---
    elif submenu == "Buscar cliente por ID.":
        st.markdown("<h3 style='color:#D4AF37;'>🔍 Buscar Cliente por ID:</h3>", unsafe_allow_html=True)
        id_buscar = st.text_input("ID cliente:").strip()
        if id_buscar:
            cliente = ClienteControlador.buscar(id_buscar)
            if cliente is None:
                st.error("❌ Cliente no encontrado. ❌")
            else:
                st.markdown('<div class="recuadro-texto" style="text-align: left !important;">', unsafe_allow_html=True)
                col_img, col_info = st.columns([35, 65])
                with col_img:
                    ruta_foto = f"imagenes/clientes/{cliente.idCliente}.jpg"
                    import os
                    if os.path.exists(ruta_foto):
                        st.image(ruta_foto, use_container_width=True)
                    else:
                        st.subheader("👤 Sin foto")
                with col_info:
                    st.markdown(f"<h4>📌 {cliente.nombres} {cliente.apellidos}</h4>", unsafe_allow_html=True)
                    st.write(f"**DNI:** {cliente.dni}")
                    st.write(f"**Email:** {cliente.email}")
                    st.write(f"**Sede:** {cliente.sucursal.nombre}")
                    st.write(f"**Estado:** {cliente.estado}")
                st.markdown('</div>', unsafe_allow_html=True)

    # --- 4. MODIFICAR CLIENTE ---
    elif submenu == "Modificar cliente.":
        st.markdown("<h3 style='color:#D4AF37;'>🔄 Modificar Cliente:</h3>", unsafe_allow_html=True)
        id_modificar = st.text_input("ID cliente a modificar:").strip()
        if id_modificar:
            cliente = ClienteControlador.buscar(id_modificar)
            if cliente is None:
                st.error("❌ Cliente no encontrado. ❌")
            else:
                st.markdown('<div class="recuadro-texto" style="text-align: left !important;">', unsafe_allow_html=True)
                st.write(f"📝 **Cliente actual:** {cliente.nombres} {cliente.apellidos}")
                
                col_m1, col_m2 = st.columns(2)
                with col_m1:
                    dni = st.text_input("Nuevo DNI:", value=cliente.dni).strip()
                    nombres = st.text_input("Nuevos nombres:", value=cliente.nombres).strip()
                    apellidos = st.text_input("Nuevos apellidos:", value=cliente.apellidos).strip()
                    direccion = st.text_input("Nueva dirección:", value=cliente.direccion).strip()
                with col_m2:
                    telefono = st.text_input("Nuevo teléfono:", value=cliente.telefono).strip()
                    email = st.text_input("Nuevo email:", value=cliente.email).strip()
                    estado = st.selectbox("Nuevo estado:", ["Activo", "Baneado"], index=0 if cliente.estado == "Activo" else 1)
                    idSucursal = st.text_input("Nueva ID Sucursal:", value=cliente.sucursal.idSucursal).strip()
                
                nueva_foto = st.file_uploader("📸 Actualizar foto de perfil (.jpg, .png)", type=["jpg", "jpeg", "png"])
                
                if st.button("🔄 Guardar Cambios"):
                    reg_ok = ClienteControlador.modificar(id_modificar, dni, nombres, apellidos, direccion, telefono, email, estado, idSucursal)
                    img_ok = False
                    
                    if nueva_foto is not None:
                        try:
                            import os
                            os.makedirs("imagenes/clientes", exist_ok=True)
                            with open(f"imagenes/clientes/{id_modificar}.jpg", "wb") as f:
                                f.write(nueva_foto.getbuffer())
                            img_ok = True
                        except Exception as e:
                            st.error(f"❌ Error al guardar la foto: {e}")
                    
                    if reg_ok or img_ok:
                        st.success("✨ ¡Cliente modificado correctamente!")
                        st.rerun()
                    else:
                        st.warning("No se alteraron valores o la ID de Sucursal ingresada no existe.")
                st.markdown('</div>', unsafe_allow_html=True)

    # --- 5. ELIMINAR CLIENTE ---
    elif submenu == "Eliminar cliente.":
        st.markdown("<h3 style='color:#FF4B4B;'>🗑️ Eliminar Cliente:</h3>", unsafe_allow_html=True)
        id_eliminar = st.text_input("ID cliente a eliminar:").strip()
        if id_eliminar:
            cliente = ClienteControlador.buscar(id_eliminar)
            if cliente is None:
                st.error("❌ Cliente no encontrado. ❌")
            else:
                st.markdown('<div class="recuadro-texto" style="border: 2px solid #FF4B4B !important; text-align: left !important;">', unsafe_allow_html=True)
                st.write(f"⚠️ **¿Está seguro de eliminar permanentemente al cliente {cliente.nombres} {cliente.apellidos}?**")
                confirmacion = st.checkbox("Confirmo que deseo realizar esta acción.")
                if st.button("❌ Eliminar Cliente"):
                    if confirmacion:
                        if ClienteControlador.eliminar(id_eliminar):
                            st.success("Cliente eliminado correctamente de la base de datos.")
                        else:
                            st.error("No se pudo eliminar el cliente.")
                st.markdown('</div>', unsafe_allow_html=True)

    # --- 6. VER CUENTAS BANCARIAS DE UN CLIENTE ---
    elif submenu == "Ver cuentas bancarias de un cliente.":
        st.markdown("<h3 style='color:#D4AF37;'>💳 Cuentas Bancarias Vinculadas:</h3>", unsafe_allow_html=True)
        id_cliente = st.text_input("Ingrese la ID del Cliente a consultar:").strip()
        
        if id_cliente:
            cliente = ClienteControlador.buscar(id_cliente)
            if cliente is None:
                st.error("❌ Cliente no encontrado.")
            else:
                st.markdown(f"<h4>👤 Cuentas de: {cliente.nombres} {cliente.apellidos}</h4>", unsafe_allow_html=True)
                cuentas = ClienteControlador.listar_cuentas_cliente(id_cliente)
                
                if not cuentas:
                    st.info("Este cliente no posee cuentas bancarias asociadas en este momento.")
                else:
                    for cta in cuentas:
                        st.markdown(f"""
                            <div class="recuadro-texto" style="margin: 5px 0px; padding: 12px; text-align: left !important;">
                                <b style="color:#D4AF37;">💳 N° Cuenta: {getattr(cta, 'nroCuenta', 'N/A')}</b> | 
                                <span style="color:#FFFFFF;">Tipo: {getattr(cta, 'tipoCuenta', 'N/A')}</span> | 
                                <span style="color:#00FF00;">Saldo: S/. {getattr(cta, 'saldo', 0.0):.2f}</span>
                            </div>
                        """, unsafe_allow_html=True)

# -----------------------------------------------------------------------------------------------------------
# Vamos 
# CUENTA BANCARIAS Y OPERACIONES(TRANSACCIONES)...
elif opcion_principal == "Cuentas Bancarias y Operaciones":
    st.markdown("<h1 style='color:#FFFFFF; margin-bottom: 5px;'>💳 Cuentas Bancarias y Operaciones:</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#A0AEC0; font-size:14px;'>Módulo unificado de servicios financieros, transacciones en firme y auditoría mediante Machine Learning.</p>", unsafe_allow_html=True)
    st.write("---")

    # --- ABRIR CUENTA BANCARIA ---
    if submenu == "Abrir cuenta bancaria.":
        st.markdown("<h3 style='color:#D4AF37;'>✍️ Formulario de Apertura de Cuenta Bancaria:</h3>", unsafe_allow_html=True)
        st.markdown('<div class="recuadro-texto" style="text-align: left !important;">', unsafe_allow_html=True)
        
        col_c1, col_c2 = st.columns(2)
        with col_c1:
            idCuenta = st.text_input("ID de la Cuenta (Código interno):", placeholder="Ej. CB0001").strip()
            numeroCuenta = st.text_input("Número de Cuenta Único (Local / CCI):", placeholder="Ej. 191-XXXXXXXX-X-XX").strip()
            tipoCuenta = st.selectbox("Tipo de Cuenta Bancaria:", ["Ahorros", "Corriente"])
        with col_c2:
            saldo = st.number_input("Monto / Depósito de Apertura (S/.):", min_value=0.0, step=50.0, format="%.2f")
            fechaApertura = st.text_input("Fecha de Registro (AAAA-MM-DD):", value=datetime.now().strftime("%Y-%m-%d")).strip()
            idCliente = st.text_input("ID del Cliente Titular (Dueño de la cuenta):").strip()
            
        if st.button("Registrar y Validar Apertura...", type="primary"):
            if not idCuenta or not numeroCuenta or not idCliente:
                st.error("Los campos ID Cuenta, Número de Cuenta e ID de Cliente Titular no pueden quedar vacíos.")
            else:
                # El controlador valida internamente si el cliente existe en el sistema
                if CuentaControlador.registrar(idCuenta, numeroCuenta, tipoCuenta, saldo, fechaApertura, "Activa", idCliente):
                    st.success(f"¡La cuenta {numeroCuenta} ha sido asignada al cliente {idCliente} con éxito!")
                else:
                    st.error("❌ No se pudo aperturar la cuenta. Verifique que el ID no esté duplicado o que el Cliente exista en los registros. ❌")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- LISTAR TODAS LAS CUENTAS ---
    elif submenu == "Listar todas las cuentas.":
        st.markdown("<h3 style='color:#D4AF37;'>📋 Registro General de Cuentas del Banco:</h3>", unsafe_allow_html=True)
        cuentas = CuentaControlador.listar()
        
        if not cuentas:
            st.info("No se registran cuentas bancarias creadas en la base de datos.")
        else:
            datos_tabla = []
            for cta in cuentas:
                datos_tabla.append({
                    "ID Interno": cta.idCuenta,
                    "Número Cuenta": cta.numeroCuenta,
                    "Tipo de Cuenta": cta.tipoCuenta,
                    "Saldo Disponible": f"S/. {cta.saldo:.2f}",
                    "Fecha Apertura": cta.fechaApertura,
                    "Estado Actual": cta.estado,
                    "Titular / DNI": f"{cta.cliente.nombres} {cta.cliente.apellidos} ({cta.cliente.idCliente})"
                })
            
            df_cuentas = pd.DataFrame(datos_tabla)
            st.dataframe(df_cuentas, use_container_width=True, hide_index=True)
            st.caption(f"Análisis descriptivo: {len(cuentas)} registros financieros indexados.")

    # --- CONSULTAR CUENTA POR ID (VER SALDO) ---
    elif submenu == "Consultar cuenta por ID (Ver saldo).":
        st.markdown("<h3 style='color:#D4AF37;'>🔍 Módulo de Consulta de Saldos:</h3>", unsafe_allow_html=True)
        id_buscar = st.text_input("Ingrese la clave o ID de Cuenta a auditar:").strip()
        
        if id_buscar:
            cuenta = CuentaControlador.buscar(id_buscar)
            if cuenta is None:
                st.error("❌ Registro no encontrado. Intente con otra identificación válida.")
            else:
                st.markdown('<div class="recuadro-texto" style="text-align: left !important;">', unsafe_allow_html=True)
                st.markdown(f"<h4>📌 Cuenta: {cuenta.numeroCuenta}</h4>", unsafe_allow_html=True)
                st.write(f"**Cliente Asociado:** {cuenta.cliente.nombres} {cuenta.cliente.apellidos}")
                st.write(f"**Tipo de Contrato:** Cuenta de {cuenta.tipoCuenta}")
                st.write(f"**Antigüedad:** Creada el {cuenta.fechaApertura}")
                
                if cuenta.estado.strip().capitalize() == "Activo":
                    st.markdown("<p style='color:#00FF00; margin:0;'><b>🟢 Estado del Canal:</b> Operando Activo</p>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<p style='color:#FF4B4B; margin:0;'><b>🔴 Estado del Canal:</b> {cuenta.estado}</p>", unsafe_allow_html=True)
                
                st.write("---")
                st.metric(label="Balance Líquido en Caja", value=f"S/. {cuenta.saldo:.2f}")
                st.markdown('</div>', unsafe_allow_html=True)

    # --- TRANSACCIONES: DEPÓSITO, RETIRO Y TRANSFERENCIA (INTEGRACIÓN CON MACHINE LEARNING) ---
    elif submenu in ["Realizar Depósito.", "Realizar Retiro.", "Realizar Transferencia."]:
        tipo_op = "Depósito" if "Depósito" in submenu else ("Retiro" if "Retiro" in submenu else "Transferencia")
        
        st.markdown(f"<h3 style='color:#D4AF37;'>Transacción en Ventanilla Virtual: {tipo_op}</h3>", unsafe_allow_html=True)
        st.markdown('<div class="recuadro-texto" style="text-align: left !important;">', unsafe_allow_html=True)
        
        idCuenta = st.text_input("ID de la Cuenta de Origen/Operación:").strip()
        idDestino = st.text_input("ID de la Cuenta Destino / Beneficiario Interbancario:").strip() if tipo_op == "Transferencia" else ""
        monto = st.number_input(f"Ingrese la cantidad del {tipo_op} (S/.):", min_value=0.01, step=20.0, format="%.2f")
        
        if st.button(f"Ejecutar Operación de {tipo_op}", type="primary"):
            cuenta_obj = CuentaControlador.buscar(idCuenta)
            
            # Validaciones lógicas básicas 
            if cuenta_obj is None:
                st.error("❌ Operación denegada. La cuenta especificada no está registrada en el núcleo del sistema. ❌ ")
            elif cuenta_obj.estado.strip().capitalize() != "Activo":
                st.error(f"❌ Transacción cancelada. El canal financiero está restringido bajo estado: {cuenta_obj.estado} ❌ ")
            elif tipo_op in ["Retiro", "Transferencia"] and cuenta_obj.saldo < monto:
                st.error(f"❌ Fondos insuficientes. Su saldo actual es de S/. {cuenta_obj.saldo:.2f} y requiere S/. {monto:.2f} ❌ ")
            else:
                # LLAMADA MODELO DE INTELIGENCIA ARTIFICIAL (_PaquitoNuevasAmericasBank_ia)
                prob_fraude, veredicto = FiltroAntifraude.es_operacion_sospechosa(monto, tipo_op, cuenta_obj.saldo)
                
                st.markdown("#### 🧠 Score de Seguridad de Inteligencia Artificial:")
                st.progress(prob_fraude / 100.0)
                
                if veredicto == "BLOQUEADO":
                    st.error(f"**¡ALERTA MÁXIMA DE FRAUDE! El Veredicto de la IA es: {veredicto}**")
                    st.warning(f"Riesgo de suplantación/fraude estimado: **{prob_fraude:.2f}%** (Umbral crítico $\geq$ 75%)")
                    
                    # Ciberseguridad Activa: 
                    # Se ha decidido CONGELAR la cuenta en la Base de Datos para evitar pérdidas y otros problemas.
                    cuenta_obj.estado = "Congelada"
                    CuentaBancariaDAO.actualizar(cuenta_obj)
                    
                    # Se ha guardado la traza analítica en el historia de auditoría legales 
                    TransaccionControlador.registrar_movimiento(idCuenta, tipo_op, monto, prob_fraude, veredicto)
                    
                    st.error("Protocolo preventivo ejecutado: La cuenta bancaria ha sido **Congelada** automáticamente.")
                else:
                    st.success(f"**Veredicto de Seguridad: {veredicto}**")
                    st.info(f"Índice de anomalías detectado: **{prob_fraude:.2f}%**. Operación considerada de confianza. Eres un gran usuario.")
                    
                    # SI LA IA DA LUZ VERDE, SE PROCEDE CON LA PERSISTENCIA EN LA BASE DE DATOS DE LA OPERACION
                    if tipo_op == "Depósito":
                        ejecutado = CuentaControlador.depositar(idCuenta, monto)
                    elif tipo_op == "Retiro":
                        ejecutado = CuentaControlador.retirar(idCuenta, monto)
                    else:
                        ejecutado = CuentaControlador.transferir(idCuenta, idDestino, monto)
                        
                    if ejecutado:
                        # HISTORIZACIÓN AUTOMÁTICA EN LA TABLA DE TRANSACCIONES
                        TransaccionControlador.registrar_movimiento(idCuenta, tipo_op, monto, prob_fraude, veredicto)
                        st.success(f"¡El {tipo_op} por S/. {monto:.2f} fue procesado y asentado en los libros contables!¡Muchas gracias por confiar en nosotros!")
                    else:
                        st.error("Error crítico de sincronización al actualizar los saldos maestros de la cuenta...")
        st.markdown('</div>', unsafe_allow_html=True)

    # --- VER HISTORIAL DE TRANSACCIONES (DATOS REALES DESDE LA BASE DE DATOS EN MYSQL WORKBENCH) ---
    elif submenu == "Ver historial de transacciones de la cuenta...":
        st.markdown("<h3 style='color:#D4AF37;'>🤖 Panel de Auditoría Predictiva (Machine Learning)</h3>", unsafe_allow_html=True)
        st.write("Cada movimiento histórico es analizado dinámicamente en tiempo real por el modelo inteligente del banco.")

        idCuenta_buscar = st.text_input("Ingrese el ID de la Cuenta Bancaria (Ej: CB0001, CB0002, CB0007):").strip()

        if idCuenta_buscar:
            from bd.conexion import Conexion
            from mysql.connector import Error
            # Importamos tu clase de Machine Learning (Ajusta la ruta si tu archivo se llama diferente)
            from controladores.guardian_fraudes import FiltroAntifraude
            
            historial_real = []
            saldo_actual_cuenta = 0.0
            
            conexion = Conexion.obtener_conexion() if hasattr(Conexion, 'obtener_conexion') else Conexion.obtainer_conexion()
            cursor = conexion.cursor() if conexion else None
            
            if conexion and cursor:
                try:
                    # 1. Obtenemos primero el saldo de la cuenta para nutrir con precisión el modelo de ML
                    query_saldo = "SELECT saldo FROM CUENTA_BANCARIA WHERE idCuenta = %s;"
                    cursor.execute(query_saldo, (idCuenta_buscar,))
                    res_saldo = cursor.fetchone()
                    if res_saldo:
                        saldo_actual_cuenta = float(res_saldo[0])

                    # 2. Extraemos las transacciones con tus columnas exactas de MySQL
                    query_trans = """
                        SELECT idTransaccion, tipoTransaccion, monto, fecha, descripcion, idBeneficiario 
                        FROM TRANSACCION 
                        WHERE idCuenta = %s 
                        ORDER BY fecha DESC;
                    """
                    cursor.execute(query_trans, (idCuenta_buscar,))
                    for reg in cursor.fetchall():
                        f_str = reg[3].strftime("%Y-%m-%d") if hasattr(reg[3], "strftime") else str(reg[3])
                        historial_real.append({
                            "id": reg[0],
                            "tipo": reg[1],
                            "monto": float(reg[2]),
                            "fecha": f_str,
                            "descripcion": reg[4],
                            "beneficiario": reg[5] if reg[5] else "N/A"
                        })
                except Error as e:
                    st.error(f"Error de base de datos: {e}")
                finally:
                    Conexion.cerrar_recursos(conexion, cursor)
            
            # 3. Procesar las filas e inyectarle el Machine Learning Real
            if not historial_real:
                st.warning(f"ℹ️ No se encontraron movimientos o la cuenta '{idCuenta_buscar}' no existe.")
            else:
                filas_transacciones_html = ""
                for t in historial_real:
                    
                    # 🧠 EJECUCIÓN EN VIVO DEL MACHINE LEARNING CON TU FILTRO
                    # Le pasamos el monto de la transacción, el tipo y el saldo recuperado de la BD
                    score_fraude, veredicto_ml = FiltroAntifraude.es_operacion_sospechosa(
                        monto=t["monto"], 
                        tipo_texto=t["tipo"], 
                        saldo_cuenta=saldo_actual_cuenta
                    )
                    
                    # Diseño de Badges dinámicos según lo que dicte el veredicto real del algoritmo
                    if veredicto_ml == "BLOQUEADO" or score_fraude >= 75.0:
                        badge_veredicto = f"<span style='background-color: #EF4444; color: #FFFFFF; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;'>⚠️ {veredicto_ml}</span>"
                    elif score_fraude >= 40.0:
                        badge_veredicto = f"<span style='background-color: #F59E0B; color: #FFFFFF; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;'>⚡ REVISIÓN</span>"
                    else:
                        badge_veredicto = f"<span style='background-color: #22C55E; color: #FFFFFF; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: bold;'>✅ {veredicto_ml}</span>"

                    # Colores estéticos para diferenciar depósitos de salidas de dinero
                    if t["tipo"] == "Depósito":
                        badge_tipo = "<span style='background-color: #22C55E; color: #FFFFFF; padding: 3px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;'>Depósito</span>"
                        color_monto = "#22C55E"
                        signo = "+"
                    elif t["tipo"] == "Retiro":
                        badge_tipo = "<span style='background-color: #EF4444; color: #FFFFFF; padding: 3px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;'>Retiro</span>"
                        color_monto = "#EF4444"
                        signo = "-"
                    else:
                        badge_tipo = "<span style='background-color: #3B82F6; color: #FFFFFF; padding: 3px 6px; border-radius: 4px; font-weight: bold; font-size: 11px;'>Transferencia</span>"
                        color_monto = "#3B82F6"
                        signo = "-"

                    filas_transacciones_html += f"<tr><td><strong>{t['id']}</strong></td><td>{t['fecha']}</td><td>{badge_tipo}</td><td style='color: {color_monto}; font-weight: bold;'>{signo} S/. {t['monto']:.2f}</td><td style='font-family: monospace; font-weight: bold;'>{score_fraude:.2f}%</td><td>{badge_veredicto}</td><td>{t['descripcion']}</td></tr>"

                # 4. Construcción compacta de la tabla en una sola línea para evitar problemas de texto plano
                html_tabla_historial = "<style>.tabla-ml-real { width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; background-color: #FFFFFF !important; border-radius: 6px; overflow: hidden; margin-top: 15px; } .tabla-ml-real th { background-color: #000000 !important; color: #FFFFFF !important; font-weight: bold; padding: 12px; text-align: left; border: 1px solid #333333; font-size: 13px; } .tabla-ml-real td { background-color: #FFFFFF !important; color: #000000 !important; padding: 12px; border: 1px solid #E0E0E0; font-size: 12.5px; } .tabla-ml-real tr:nth-child(even) td { background-color: #F8F9FA !important; }</style><table class='tabla-ml-real'><thead><tr><th>ID</th><th>Fecha</th><th>Tipo Op.</th><th>Monto</th><th>% Score Fraude</th><th>Veredicto Paquito IA</th><th>Descripción</th></tr></thead><tbody>" + filas_transacciones_html + "</tbody></table>"
                
                st.markdown(html_tabla_historial, unsafe_allow_html=True)
    # ---CANCELAR/ELIMINAR CUENTA ---
    elif submenu == "Cancelar/Eliminar cuenta.":
        st.markdown("<h3 style='color:#FF4B4B;'>🗑️ Liquidación y Baja del Registro de Cuentas:</h3>", unsafe_allow_html=True)
        id_eliminar = st.text_input("Ingrese el ID de la Cuenta a cerrar definitivamente:").strip()
        
        if id_eliminar:
            cuenta = CuentaControlador.buscar(id_eliminar)
            if cuenta is None:
                st.error("❌ No se encontró la cuenta que desea dar de baja. ❌")
            else:
                st.markdown('<div class="recuadro-texto" style="border: 2px solid #FF4B4B !important; text-align: left !important;">', unsafe_allow_html=True)
                st.write(f"⚠️ **Aviso de Seguridad:** Va a eliminar la cuenta **{cuenta.numeroCuenta}** ligada a **{cuenta.cliente.nombres} {cuenta.cliente.apellidos}**.")
                st.write(f"Fondos remanentes a liquidar en ventanilla física: **S/. {cuenta.saldo:.2f}**")
                
                confirmacion = st.checkbox("Acepto que esta acción purgará de forma definitiva la cuenta y sus relaciones históricas en cascada.")
                
                if st.button("Proceder con la Destrucción del Registro"):
                    if confirmacion:
                        if CuentaControlador.eliminar(id_eliminar):
                            st.success("🔥 Cuenta bancaria dada de baja del sistema principal. Gracias por su tiempo con nosotros.")
                        else:
                            st.error("No se pudo ejecutar la acción. Verifique restricciones de integridad en la Base de Datos.")
                    else:
                        st.warning("Es mandatorio marcar el check de confirmación de responsabilidades antes de borrar los datos.")
                st.markdown('</div>', unsafe_allow_html=True)


# -----------------------------------------------------------------------------------------------------------
# Vamos 
# PRÉSTAMOS...
elif "Préstamos" in opcion_principal:
    st.markdown("<h1 style='color:#FFFFFF; margin-bottom: 5px;'>💰 Gestión de Préstamos:</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#A0AEC0; font-size:14px;'>Evaluación de créditos, aprobación de fondos y control de amortizaciones...</p>", unsafe_allow_html=True)
    st.write("---")

    # --- 1. SOLICITAR / REGISTRAR PRÉSTAMO ---
    if submenu == "Solicitar/Registrar préstamo.":
        st.markdown("<h3 style='color:#D4AF37;'>✍️ Nueva Solicitud de Crédito:</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            idPrestamo = st.text_input("Código de Préstamo (Ej: P00001):").strip()
            monto = st.number_input("Monto Solicitado (S/.):", min_value=0.0, step=100.0)
            tasaInteres = st.number_input("Tasa de Interés Anual (%):", min_value=0.0, step=0.5)
            plazoMeses = st.number_input("Plazo del Crédito (Meses):", min_value=1, step=1)
        with col2:
            fechaPrestamo = st.text_input("Fecha de Solicitud (AAAA-MM-DD):").strip()
            estado = st.selectbox("Estado:", ["Pendiente", "Aprobado", "Rechazado", "Vigente", "Pagado"])
            idCliente = st.text_input("Código del Cliente Solicitante:").strip()
            idEmpleado = st.text_input("Código del Empleado Evaluador:").strip()
            
        if st.button("🚀 Registrar Solicitud de Préstamo", use_container_width=True):
            if not idPrestamo or not idCliente or not idEmpleado:
                st.error("⚠️ Todos los campos con códigos son obligatorios.")
            else:
                exito = PrestamoControlador.registrar(idPrestamo, monto, tasaInteres, plazoMeses, fechaPrestamo, estado, idCliente, idEmpleado)
                if exito:
                    st.success(f"El préstamo {idPrestamo} ha sido registrado de manera exitosa.")
                else:
                    st.error("❌ No se pudo registrar. Verifique que el ID de Cliente y Empleado existan. ❌")

    # --- 2. LISTAR TODOS LOS PRÉSTAMOS ---
    elif submenu == "Listar todos los préstamos.":
        st.markdown("<h3 style='color:#D4AF37;'>📋 Historial Global de Créditos:</h3>", unsafe_allow_html=True)
        
        lista_prestamos = PrestamoControlador.listar()
        
        if not lista_prestamos:
            st.info("No se registran solicitudes de préstamos en el sistema.")
        else:
            datos_tabla = []
            for p in lista_prestamos:
                datos_tabla.append({
                    "ID Préstamo": p.idPrestamo,
                    "Cliente": f"{p.cliente.nombres} {p.cliente.apellidos}",
                    "Monto (S/.)": f"{p.monto:.2f}",
                    "Tasa (%)": f"{p.tasaInteres:.2f}%",
                    "Plazo": f"{p.plazoMeses} meses",
                    "Fecha Registro": p.fechaPrestamo,
                    "Estado": p.estado,
                    "Evaluador": f"{p.empleado.nombres} {p.empleado.apellidos}"
                })
            
            import pandas as pd
            df_prestamos = pd.DataFrame(datos_tabla)
            
            estilo_tabla_personalizada = """
            <style>
                .tabla-prestamos {
                    width: 100%;
                    border-collapse: collapse;
                    margin: 15px 0;
                    font-size: 14px;
                    font-family: Arial, sans-serif;
                    background-color: #FFFFFF;
                }
                .tabla-prestamos th {
                    background-color: #000000 !important;
                    color: #FFFFFF !important;
                    font-weight: bold;
                    padding: 12px;
                    text-align: left;
                    border: 1px solid #333333;
                }
                .tabla-prestamos td {
                    background-color: #FFFFFF !important;
                    color: #000000 !important;
                    padding: 10px;
                    border: 1px solid #E0E0E0;
                }
                .tabla-prestamos tr:nth-child(even) td {
                    background-color: #F9F9F9 !important;
                }
            </style>
            """
            st.markdown(estilo_tabla_personalizada, unsafe_allow_html=True)
            
            html_tabla = df_prestamos.to_html(classes="tabla-prestamos", index=False, escape=False)
            st.markdown(html_tabla, unsafe_allow_html=True)

    # --- 3. BUSCAR PRÉSTAMO POR ID ---
    elif submenu == "Buscar préstamo por ID.":
        st.markdown("<h3 style='color:#D4AF37;'>🔍 Consulta de Préstamo Individual:</h3>", unsafe_allow_html=True)
        id_buscar = st.text_input("Ingrese el Código del Préstamo a consultar:").strip()
        
        if id_buscar:
            p = PrestamoControlador.buscar(id_buscar)
            if p is None:
                st.error("❌ El préstamo solicitado no existe en el sistema.")
            else:
                # Armamos una mini-tabla para mostrar el resultado único con el mismo estilo
                datos_individual = [{
                    "ID Préstamo": p.idPrestamo,
                    "Cliente": f"{p.cliente.nombres} {p.cliente.apellidos}",
                    "Monto (S/.)": f"{p.monto:.2f}",
                    "Tasa (%)": f"{p.tasaInteres:.2f}%",
                    "Plazo": f"{p.plazoMeses} meses",
                    "Fecha Registro": p.fechaPrestamo,
                    "Estado": p.estado,
                    "Evaluador": f"{p.empleado.nombres} {p.empleado.apellidos}"
                }]
                import pandas as pd
                df_individual = pd.DataFrame(datos_individual)
                
                estilo_tabla_personalizada = """
                <style>
                    .tabla-prestamos { width: 100%; border-collapse: collapse; margin: 15px 0; font-size: 14px; font-family: Arial, sans-serif; background-color: #FFFFFF; }
                    .tabla-prestamos th { background-color: #000000 !important; color: #FFFFFF !important; font-weight: bold; padding: 12px; text-align: left; border: 1px solid #333333; }
                    .tabla-prestamos td { background-color: #FFFFFF !important; color: #000000 !important; padding: 10px; border: 1px solid #E0E0E0; }
                </style>
                """
                st.markdown(estilo_tabla_personalizada, unsafe_allow_html=True)
                html_tabla = df_individual.to_html(classes="tabla-prestamos", index=False, escape=False)
                st.markdown(html_tabla, unsafe_allow_html=True)

    # --- ACCIÓN 4: CAMBIAR ESTADO DE PRÉSTAMO ---
    elif submenu == "Cambiar estado de préstamo (Aprobar/Liquidar).":
        st.markdown("<h3 style='color:#D4AF37;'>⚙️ Cambiar Estado del Crédito:</h3>", unsafe_allow_html=True)
        
        id_buscar = st.text_input("Ingrese el Código del Préstamo a Gestionar:").strip()
        if id_buscar:
            prestamo = PrestamoControlador.buscar(id_buscar)
            if prestamo is None:
                st.error("❌ El préstamo solicitado no existe.")
            else:
                st.info(f"**Detalles Actuales:** Cliente: {prestamo.cliente.nombres} | Monto: S/. {prestamo.monto:.2f} | Estado actual: **{prestamo.estado}**")
                nuevo_estado = st.selectbox("Seleccione el Nuevo Estado:", ["Pendiente", "Aprobado", "Rechazado", "Vigente", "Pagado"])
                
                if st.button("💾 Actualizar Estado"):
                    if PrestamoControlador.actualizar_estado(id_buscar, nuevo_estado):
                        st.success(f"🎉 El estado del préstamo {id_buscar} se cambió a '{nuevo_estado}' con éxito.")
                    else:
                        st.error("❌ Error interno al intentar cambiar el estado.")

    # --- 5. ELIMINAR REGISTRO DE PRÉSTAMO ---
    elif submenu == "Eliminar registro de préstamo.":
        st.markdown("<h3 style='color:#FF4B4B;'>🗑️ Eliminar Registro de Préstamo</h3>", unsafe_allow_html=True)
        id_eliminar = st.text_input("Ingrese el Código del Préstamo a remover:").strip()
        
        if id_eliminar:
            st.warning(f"⚠️ ¿Está completamente seguro de que desea eliminar el registro del préstamo {id_eliminar}?")
            if st.button("💥 Confirmar Eliminación Permanente", use_container_width=True):
                if PrestamoControlador.eliminar(id_eliminar):
                    st.success("🗑️ Registro eliminado satisfactoriamente de la base de datos.")
                else:
                    st.error("❌ No se pudo eliminar el registro. Verifique el código. ❌")


# -----------------------------------------------------------------------------------------------------------
# Vamos 
# BENEFICIARIOS...
elif "Beneficiarios" in opcion_principal:
    st.markdown("<h1 style='color:#FFFFFF; margin-bottom: 5px;'>👥 Agenda de Beneficiarios</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color:#A0AEC0; font-size:14px;'>Gestión de cuentas frecuentes para transferencias interbancarias inmediatas.</p>", unsafe_allow_html=True)
    st.write("---")

    # --- 1. AGREGAR BENEFICIARIO ---
    if submenu == "Agregar beneficiario frecuente.":
        st.markdown("<h3 style='color:#D4AF37;'>Registrar Beneficiario Frecuente:</h3>", unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            idBeneficiario = st.text_input("Código Beneficiario (Ej: BF0001):").strip()
            nombres = st.text_input("Nombres:").strip()
            apellidos = st.text_input("Apellidos:").strip()
        with col2:
            num_cuenta = st.text_input("Número de Cuenta Externa:").strip()
            banco_dest = st.selectbox("Banco Destino:", ["BCP", "BBVA", "Interbank", "Scotiabank", "BanBif", "Banco de la Nación"])
            
        if st.button("Guardar en Agenda...", width="stretch"):
            if not idBeneficiario or not nombres or not apellidos or not num_cuenta:
                st.error("Todos los campos son obligatorios para el registro.")
            else:
                if BeneficiarioControlador.registrar(idBeneficiario, nombres, apellidos, num_cuenta, banco_dest):
                    st.success(f"✅ El beneficiario {nombres} {apellidos} fue añadido con éxito.")
                else:
                    st.error("❌ No se pudo registrar. Verifique si el ID ya existe. ❌")

    # --- 2. LISTAR BENEFICIARIOS (CON COLUMNA ROTADA DE COSTADO) ---
    elif submenu == "Listar mis beneficiarios.":
        st.markdown("<h3 style='color:#D4AF37;'>📋 Mis Beneficiarios Registrados:</h3>", unsafe_allow_html=True)
        
        lista_ben = BeneficiarioControlador.listar()
        
        if not lista_ben:
            st.info("Tu agenda de beneficiarios se encuentra vacía.")
        else:
            col_tabla, col_banner = st.columns([8, 2])
            
            with col_tabla:
                # 1. ARMANDO LAS FILAS DE LA TABLA
                filas_html = ""
                for b in lista_ben:
                    filas_html += f"<tr><td><strong>{b.idBeneficiario}</strong></td><td>{b.nombres}</td><td>{b.apellidos}</td><td style='font-family: monospace;'>{b.numeroCuenta}</td><td><span style='background-color: #E2E8F0; color: #1A202C; padding: 4px 8px; border-radius: 4px; font-weight: bold;'>{b.bancoDestino}</span></td></tr>"
                
                # 2. TABLA
                html_final_tabla = f"""
                <style>
                    .tabla-format-banco {{
                        width: 100%;
                        border-collapse: collapse;
                        font-family: 'Segoe UI', Arial, sans-serif;
                        background-color: #FFFFFF !important;
                        border-radius: 8px;
                        overflow: hidden;
                    }}
                    .tabla-format-banco th {{
                        background-color: #000000 !important;
                        color: #FFFFFF !important;
                        font-weight: bold;
                        padding: 14px 12px;
                        text-align: left;
                        font-size: 14px;
                        border: 1px solid #333333;
                    }}
                    .tabla-format-banco td {{
                        background-color: #FFFFFF !important;
                        color: #000000 !important;
                        padding: 12px;
                        border: 1px solid #E0E0E0;
                        font-size: 13.5px;
                    }}
                    .tabla-format-banco tr:nth-child(even) td {{
                        background-color: #F9F9F9 !important;
                    }}
                </style>
                <table class='tabla-format-banco'>
                    <thead>
                        <tr>
                            <th>ID Beneficiario</th>
                            <th>Nombres</th>
                            <th>Apellidos</th>
                            <th>N° Cuenta Externa</th>
                            <th>Banco</th>
                        </tr>
                    </thead>
                    <tbody>
                        {filas_html}
                    </tbody>
                </table>
                """
                # Enviamos el bloque completo
                st.markdown(html_final_tabla, unsafe_allow_html=True)
            
            with col_banner:
                # 2. Columna del costado derecho con el texto vertical gigante CONEXION CON OTROS BANCOS
                estilos_banner = """
                <style>
                    .contenedor-banner-derecho {
                        display: flex;
                        background-color: #111111;
                        color: #D4AF37;
                        border: 1px solid #333333;
                        border-radius: 8px;
                        height: 100%;
                        min-height: 300px;
                        align-items: center;
                        justify-content: center;
                        text-align: center;
                        padding: 20px 5px;
                        box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    }
                    .texto-vertical-bancos {
                        writing-mode: vertical-rl;
                        transform: rotate(180deg);
                        font-size: 22px;
                        font-weight: bold;
                        letter-spacing: 4px;
                        text-transform: uppercase;
                        white-space: nowrap;
                    }
                </style>
                """
                st.markdown(estilos_banner, unsafe_allow_html=True)
                
                html_banner_final = """
                <div class='contenedor-banner-derecho'>
                    <div class='texto-vertical-bancos'>conexión con otros bancos</div>
                </div>
                """
                st.markdown(html_banner_final, unsafe_allow_html=True)

    # --- 3. BUSCAR BENEFICIARIO POR ID ---
    elif submenu == "Buscar beneficiario por ID.":
        st.markdown("<h3 style='color:#D4AF37;'>🔍 Consultar Beneficiario:</h3>", unsafe_allow_html=True)
        id_buscar = st.text_input("Ingrese el Código del Beneficiario:").strip()
        
        if id_buscar:
            b = BeneficiarioControlador.buscar(id_buscar)
            if b is None:
                st.error("❌ El beneficiario ingresado no existe en tu agenda. ❌")
            else:
                # RENDERIZADO
                estilo_tabla_beneficiarios = "<style>.tabla-beneficiarios { width: 85%; border-collapse: collapse; background-color: #FFFFFF; } .tabla-beneficiarios th { background-color: #000000 !important; color: #FFFFFF !important; font-weight: bold; padding: 12px; border: 1px solid #333333; } .tabla-beneficiarios td { background-color: #FFFFFF !important; color: #000000 !important; padding: 10px; border: 1px solid #E0E0E0; } .columna-lateral-bancos { width: 15%; background-color: #1A1A1A; color: #D4AF37; display: flex; align-items: center; justify-content: center; border: 1px solid #333333; text-align: center; } .texto-rotado { writing-mode: vertical-rl; transform: rotate(180deg); font-size: 16px; font-weight: bold; letter-spacing: 1px; text-transform: uppercase; } .contenedor-tabla-ben { display: flex; width: 100%; margin: 15px 0; }</style>"
                st.markdown(estilo_tabla_beneficiarios, unsafe_allow_html=True)
                
                tabla_html = f"""
                <div class='contenedor-tabla-ben'>
                    <table class='tabla-beneficiarios'>
                        <thead>
                            <tr>
                                <th>ID Beneficiario</th>
                                <th>Nombres</th>
                                <th>Apellidos</th>
                                <th>N° Cuenta Externa</th>
                                <th>Banco</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td>{b.idBeneficiario}</td>
                                <td>{b.nombres}</td>
                                <td>{b.apellidos}</td>
                                <td>{b.numeroCuenta}</td>
                                <td><strong>{b.bancoDestino}</strong></td>
                            </tr>
                        </tbody>
                    </table>
                    <div class='columna-lateral-bancos'><div class='texto-rotado'>en conexion con otros bancos</div></div>
                </div>
                """
                st.markdown(tabla_html, unsafe_allow_html=True)

    # --- 4. MODIFICAR BENEFICIARIO ---
    elif submenu == "Modificar datos de beneficiario.":
        st.markdown("<h3 style='color:#D4AF37;'>📝 Actualizar Datos de Beneficiario:</h3>", unsafe_allow_html=True)
        id_modificar = st.text_input("Ingrese el Código del Beneficiario a cambiar:").strip()
        
        if id_modificar:
            b = BeneficiarioControlador.buscar(id_modificar)
            if b is None:
                st.error("❌ No se encontró ningún beneficiario registrado con ese código.")
            else:
                st.info(f"**Beneficiario actual:** {b.nombres} {b.apellidos} | Cuenta actual: {b.numeroCuenta}")
                
                col1, col2 = st.columns(2)
                with col1:
                    nuevo_nombres = st.text_input("Nuevos Nombres:", value=b.nombres).strip()
                    nuevo_apellidos = st.text_input("Nuevos Apellidos:", value=b.apellidos).strip()
                with col2:
                    nueva_cuenta = st.text_input("Nuevo Número de Cuenta:", value=b.numeroCuenta).strip()
                    nuevo_bco = st.selectbox("Nuevo Banco:", ["BCP", "BBVA", "Interbank", "Scotiabank", "BanBif", "Banco de la Nación"], index=["BCP", "BBVA", "Interbank", "Scotiabank", "BanBif", "Banco de la Nación"].index(b.bancoDestino) if b.bancoDestino in ["BCP", "BBVA", "Interbank", "Scotiabank", "BanBif", "Banco de la Nación"] else 0)
                
                if st.button("💾 Guardar Cambios", width="stretch"):
                    if BeneficiarioControlador.modificar(id_modificar, nuevo_nombres, nuevo_apellidos, nueva_cuenta, nuevo_bco):
                        st.success("🎉 Datos de la agenda actualizados exitosamente.")
                    else:
                        st.error("❌ Ocurrió un error interno al intentar actualizar. ❌")

    # --- 5. ELIMINAR BENEFICIARIO ---
    elif submenu == "Eliminar beneficiario de la agenda.":
        st.markdown("<h3 style='color:#FF4B4B;'>🗑️ Eliminar de la Agenda:</h3>", unsafe_allow_html=True)
        id_elim = st.text_input("Ingrese el Código del Beneficiario a remover:").strip()
        
        if id_elim:
            b = BeneficiarioControlador.buscar(id_elim)
            if b is None:
                st.error("❌ El código ingresado no coincide con ningún beneficiario de tu agenda.")
            else:
                st.warning(f"⚠️ ¿Estás seguro de que deseas eliminar permanentemente a **{b.nombres} {b.apellidos}** de tus cuentas frecuentes?")
                if st.button("Confirmar Eliminación", width="stretch"):
                    if BeneficiarioControlador.eliminar(id_elim):
                        st.success("🗑️ El Beneficiario ha sido removido satisfactoriamente. Gracias por estar con nosotros.")
                    else:
                        st.error("❌ No se pudo completar la transacción de borrado.")

# -----------------------------------------------------------------------------------------------------------
# Vamos 
# TARJETAS...

# ========================================================
# MÓDULO: GESTIÓN DE TARJETAS (CUERPO CENTRAL)
# ========================================================
elif "Tarjetas" in opcion_principal:
    st.markdown("<h1 style='color:#FFFFFF; margin-bottom: 5px;'>💳 Sistema de Tarjetas Bancarias</h1>", unsafe_allow_html=True)
    st.write("---")

    # --- 1. EMITIR / REGISTRAR TARJETA 
    if submenu == "Emitir / Registrar tarjeta.":
        st.markdown("<h3 style='color:#D4AF37;'>🆕 Emitir Nueva Tarjeta:</h3>", unsafe_allow_html=True)
        
        # TABLA central (70%) IMAGEN de costado de las Tarjetas(30%)
        col_formulario, col_imagen_der = st.columns([7, 3])
        
        with col_formulario:
            idTarjeta = st.text_input("ID Tarjeta (Ej: TR0001):").strip()
            numeroTarjeta = st.text_input("Número de Tarjeta (16 dígitos):", max_chars=16).strip()
            tipo = st.selectbox("Tipo de Tarjeta:", ["Débito", "Crédito"])
            
            sub_col1, sub_col2 = st.columns(2)
            with sub_col1:
                fechaEmision = st.text_input("Fecha Emisión (AAAA-MM-DD):", value="2026-07-02").strip()
            with sub_col2:
                fechaVencimiento = st.text_input("Fecha Vencimiento (AAAA-MM-DD):", value="2031-07-02").strip()
                
            estado = st.selectbox("Estado Inicial:", ["Activa", "Bloqueada"])
            idCuenta = st.text_input("ID de Cuenta Bancaria asociada (Ej: CB0001):").strip()
            
            if st.button("Emitir Plástico", width="stretch"):
                if not idTarjeta or not numeroTarjeta or not idCuenta:
                    st.error("El ID, Número y Cuenta asociada son campos estrictamente obligatorios.")
                else:
                    if TarjetaControlador.registrar(idTarjeta, numeroTarjeta, tipo, fechaVencimiento, fechaEmision, estado, idCuenta):
                        st.success(f"¡Tarjeta {numeroTarjeta} emitida correctamente en el sistema!")
                    else:
                        st.error("❌ Error de emisión. Verifique que el ID de la cuenta bancaria exista en la BD. ❌")
                        
        with col_imagen_der:
            st.markdown("<div style='margin-top: 40px; text-align: center;'>", unsafe_allow_html=True)
            st.image("imagenes/tarjetas/tarjetas1.png", caption="Lector de Tarjetas Integrado...", width=220)
            st.markdown("</div>", unsafe_allow_html=True)

    # --- 2. LISTAR TODAS LAS TARJETAS 
    elif submenu == "Listar todas las tarjetas.":
        # Texto LAS TARJETAS DE NUESTRO BANCO
        st.markdown("<h2 style='color:#FFFFFF; text-align: center; letter-spacing: 1px;'>LAS TARJETAS DE NUESTRO BANCO</h2>", unsafe_allow_html=True)
        
        # IMAGEN CENTRAL
        st.markdown("<div style='text-align: center; margin: 20px 0;'>", unsafe_allow_html=True)
        st.image("imagenes/tarjetas/tarjetas1.png", caption="Línea de Crédito y Débito Premium - Las Nuevas Américas.", use_container_width=True)                 
        st.markdown("</div>", unsafe_allow_html=True)
        
        tarjetas = TarjetaControlador.listar()
        
        if not tarjetas:
            st.info("No existen tarjetas emitidas en el sistema en este momento.")
        else: # LISTADO
            filas_html = ""
            for t in tarjetas:
                color_badge = "#22C55E" if t.estado == "Activa" else "#EF4444"
                filas_html += f"<tr><td><strong>{t.idTarjeta}</strong></td><td style='font-family: monospace; font-size: 14.5px; letter-spacing: 1px;'>{t.numeroTarjeta}</td><td><span style='background-color: #E2E8F0; color: #1A202C; padding: 3px 6px; border-radius: 4px; font-weight: bold;'>{t.tipoTarjeta}</span></td><td>{t.fechaEmision}</td><td>{t.fechaVencimiento}</td><td><span style='background-color: {color_badge}; color: #FFFFFF; padding: 3px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;'>{t.estado}</span></td><td>{t.cuenta.idCuenta if t.cuenta else 'N/A'}</td></tr>"
                
            html_tabla_tarjetas = "<style>.tabla-tarjetas-banco { width: 100%; border-collapse: collapse; font-family: Arial, sans-serif; background-color: #FFFFFF !important; border-radius: 6px; overflow: hidden; margin-top: 15px; } .tabla-tarjetas-banco th { background-color: #000000 !important; color: #FFFFFF !important; font-weight: bold; padding: 12px; text-align: left; border: 1px solid #333333; } .tabla-tarjetas-banco td { background-color: #FFFFFF !important; color: #000000 !important; padding: 12px; border: 1px solid #E0E0E0; } .tabla-tarjetas-banco tr:nth-child(even) td { background-color: #F8F9FA !important; }</style><table class='tabla-tarjetas-banco'><thead><tr><th>ID Tarjeta</th><th>Número de Tarjeta</th><th>Tipo</th><th>Emisión</th><th>Vencimiento</th><th>Estado</th><th>Cuenta Asociada</th></tr></thead><tbody>" + filas_html + "</tbody></table>"           
            # Renderizado 
            st.markdown(html_tabla_tarjetas, unsafe_allow_html=True)

    # --- 3. CONSULTAR TARJETA POR ID 
    elif submenu == "Consultar tarjeta por ID.":
        st.markdown("<h3 style='color:#D4AF37;'>🔍 Consultar Detalles de Tarjeta:</h3>", unsafe_allow_html=True)
        id_buscar = st.text_input("Ingrese el Código de Tarjeta (Ej: TR0001):").strip()
        
        if id_buscar:
            t = TarjetaControlador.buscar(id_buscar)
            if t is None:
                st.error("❌ La tarjeta solicitada no se encuentra registrada. ❌")
            else:
                st.success(f"💳 Tarjeta Localizada: {t.tipoTarjeta} - N° {t.numeroTarjeta}")
                st.write(f"**Fecha Emisión:** {t.fechaEmision} | **Fecha Vencimiento:** {t.fechaVencimiento}")
                st.write(f"**Estado Actual:** {t.estado} | **Cuenta Enlazada:** {t.cuenta.numeroCuenta if t.cuenta else 'Ninguna'}")

    # --- 4. MODIFICAR DATOS DE TARJETA 
    elif submenu == "Modificar datos de tarjeta.":
        st.markdown("<h3 style='color:#D4AF37;'>📝 Modificar Parámetros de Tarjeta:</h3>", unsafe_allow_html=True)
        id_mod = st.text_input("Código de Tarjeta a alterar:").strip()
        
        if id_mod:
            t = TarjetaControlador.buscar(id_mod)
            if t is None:
                st.error("❌ El ID ingresado no coincide con ninguna tarjeta activa. ❌")
            else:
                st.info(f"Modificando plástico actual: {t.numeroTarjeta}")
                num_new = st.text_input("Número de Tarjeta:", value=t.numeroTarjeta).strip()
                tipo_new = st.selectbox("Tipo:", ["Débito", "Crédito"], index=0 if t.tipoTarjeta == "Débito" else 1)
                venc_new = st.text_input("Nueva Fecha Vencimiento:", value=t.fechaVencimiento).strip()
                emis_new = st.text_input("Nueva Fecha Emisión:", value=t.fechaEmision).strip()
                est_new = st.selectbox("Estado actual:", ["Activa", "Bloqueada", "Vencida", "Cancelada"], index=["Activa", "Bloqueada", "Vencida", "Cancelada"].index(t.estado))
                id_cta_new = st.text_input("Asociar a otra Cuenta ID:", value=t.cuenta.idCuenta if t.cuenta else "").strip()
                
                if st.button("Guardar Cambios..."):
                    if TarjetaControlador.modificar(id_mod, num_new, tipo_new, venc_new, emis_new, est_new, id_cta_new):
                        st.success("🎉 Los cambios de la tarjeta se grabaron con éxito.")
                    else:
                        st.error("❌ No se pudo actualizar el registro. Valide el ID de la cuenta bancaria.")

    # --- 5. BLOQUEAR / ELIMINAR TARJETA ---
    elif submenu == "Bloquear / Eliminar tarjeta":
        st.markdown("<h3 style='color:#FF4B4B;'>🗑️ Baja del Sistema de Tarjetas</h3>", unsafe_allow_html=True)
        id_elim = st.text_input("Código de Tarjeta a remover permanentemente:").strip()
        
        if id_elim:
            t = TarjetaControlador.buscar(id_elim)
            if t is None:
                st.error("❌ Registro no encontrado.")
            else:
                st.warning(f"⚠️ ¿Confirmar la baja definitiva del plástico {t.numeroTarjeta} ({t.tipoTarjeta})?")
                if st.button("💥 Proceder a la eliminación"):
                    if TarjetaControlador.eliminar(id_elim):
                        st.success("🗑️ Tarjeta eliminada correctamente de los archivos bancarios.")
                    else:
                        st.error("❌ No se pudo concretar el borrado.")

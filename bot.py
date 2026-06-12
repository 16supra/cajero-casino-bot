import logging
from telegram import Update, ReplyKeyboardMarkup, ReplyKeyboardRemove
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes,
    ConversationHandler,
)

# 1. CONFIGURACIÓN DE LOGS (Exigido para la auditoría técnica del TPI)
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', 
    level=logging.INFO
)

# 2. VARIABLE DEL TOKEN (Corregida y aislada de la función de logs)
TOKEN = "8604704984:AAHHCeZ14WmDpCEI60iwXf_9kFR8yq7f9jA"

# 3. DICCIONARIO DE DATOS / PERSISTENCIA (Base de datos simulada de jugadores)
BASE_DATOS = {
    "123": {"nombre": "Roberto", "saldo": 50000},
    "456": {"nombre": "Gabriela Martínez", "saldo": 15000},
    "789": {"nombre": "Carlos López", "saldo": 0}
}

# 4. MÁQUINA DE ESTADOS (Fases del ConversationHandler)
INGRESAR_ID, MENU_PRINCIPAL, PROCESAR_DEPOSITO, PROCESAR_RETIRO = range(4)

# --- FASES DEL PROCESO ---

# 🏁 HITO DE INICIO: Comando /start (Muestra Lane del Bot iniciando el flujo)
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "🎰 ¡Bienvenido al Sistema de Cajero Automático del Casino UTN! 🎰\n\n"
        "Por favor, introduzca su ID de Jugador o número de documento para comenzar:",
        reply_markup=ReplyKeyboardRemove()
    )
    return INGRESAR_ID

# 🔍 TAREA DE SERVICIO: Validación de Identidad (Camino Feliz y Camino Infeliz)
async def validar_id(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    id_usuario = update.message.text.strip()
    
    # ❌ CAMINO INFELIZ: Entrada inválida (Letras en lugar de números)
    if not id_usuario.isdigit():
        await update.message.reply_text(
            "❌ Error de entrada: El ID debe contener solo números.\n"
            "Por favor, intente ingresar su ID numérico nuevamente:"
        )
        return INGRESAR_ID

    # 💾 CONSULTA A LA BASE DE DATOS SIMULADA
    if id_usuario in BASE_DATOS:
        context.user_data['player_id'] = id_usuario
        jugador = BASE_DATOS[id_usuario]
        
        # Guardar datos en la memoria del bot (Gestión de Estados)
        context.user_data['saldo'] = jugador['saldo']
        context.user_data['nombre'] = jugador['nombre']
        
        await update.message.reply_text(
            f"✅ ¡Identidad Verificada!\n"
            f"Jugador: {jugador['nombre']}\n"
            f"Saldo Actual: ${jugador['saldo']} ARS"
        )
        return await mostrar_menu(update, context)
    else:
        # ❌ CAMINO INFELIZ: Usuario no registrado en el sistema
        await update.message.reply_text(
            "❌ El ID ingresado no está registrado en el casino.\n"
            "Por favor, revise el número e ingréselo de nuevo:"
        )
        return INGRESAR_ID

# 📑 MENÚ PRINCIPAL (Botones interactivos en la interfaz de Telegram)
async def mostrar_menu(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    botones = [['Cargar saldo', 'Retirar ganancias'], ['Salir']]
    teclado = ReplyKeyboardMarkup(botones, resize_keyboard=True, one_time_keyboard=True)
    
    await update.message.reply_text(
        "¿Qué transacción desea realizar hoy?",
        reply_markup=teclado
    )
    return MENU_PRINCIPAL

# 💵 FLUJO DE DEPÓSITO
async def iniciar_deposito(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "📥 Ingrese el monto en pesos ($) que desea depositar para cargar fichas:",
        reply_markup=ReplyKeyboardRemove()
    )
    return PROCESAR_DEPOSITO

async def ejecutar_deposito(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    monto_texto = update.message.text.strip()
    
    # ❌ CAMINO INFELIZ: Validación de entrada de montos
    if not monto_texto.isdigit() or int(monto_texto) <= 0:
        await update.message.reply_text("❌ Monto inválido. Ingrese un número entero mayor a 0:")
        return PROCESAR_DEPOSITO
        
    monto = int(monto_texto)
    pid = context.user_data['player_id']
    
    # Modificación en persistencia de datos simulada
    BASE_DATOS[pid]['saldo'] += monto
    context.user_data['saldo'] = BASE_DATOS[pid]['saldo']
    
    await update.message.reply_text(
        f"💵 ¡Depósito Exitoso!\n"
        f"Se han cargado ${monto} a su cuenta.\n"
        f"Nuevo Saldo Total: ${context.user_data['saldo']} ARS"
    )
    return await mostrar_menu(update, context)

# 🏧 FLUJO DE RETIRO
async def iniciar_retiro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        f"📤 Su saldo disponible para extraer es de ${context.user_data['saldo']} ARS.\n"
        f"Ingrese el monto que desea retirar:",
        reply_markup=ReplyKeyboardRemove()
    )
    return PROCESAR_RETIRO

async def ejecutar_retiro(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    monto_texto = update.message.text.strip()
    
    # ❌ CAMINO INFELIZ: Error de tipo de datos al retirar
    if not monto_texto.isdigit() or int(monto_texto) <= 0:
        await update.message.reply_text("❌ Monto inválido. Ingrese un valor numérico correcto:")
        return PROCESAR_RETIRO
        
    monto = int(monto_texto)
    saldo_actual = context.user_data['saldo']
    pid = context.user_data['player_id']
    
    # 🔀 COMPUERTA LÓGICA (GATEWAY): Validación de Regla de Negocio
    if monto <= saldo_actual:
        # CAMINO FELIZ: Fondos suficientes
        BASE_DATOS[pid]['saldo'] -= monto
        context.user_data['saldo'] = BASE_DATOS[pid]['saldo']
        
        await update.message.reply_text(
            f"✅ ¡Extracción Autorizada!\n"
            f"Retiró: ${monto} ARS\n"
            f"Saldo Restante en cuenta: ${context.user_data['saldo']} ARS\n\n"
            f"🎟️ Retire su ticket impreso en la ranura del cajero virtual."
        )
    else:
        # ❌ CAMINO INFELIZ: Fondos insuficientes
        await update.message.reply_text(
            f"🚨 Extracción Rechazada: Fondos Insuficientes.\n"
            f"Intentó retirar ${monto} ARS pero solo dispone de ${saldo_actual} ARS."
        )
        
    return await mostrar_menu(update, context)

# 🚪 HITO DE FIN: Cierre del proceso administrativo
async def salir(update: Update, context: ContextTypes.DEFAULT_TYPE) -> int:
    await update.message.reply_text(
        "👋 Gracias por utilizar el Cajero del Casino UTN. ¡Buena suerte en sus jugadas!",
        reply_markup=ReplyKeyboardRemove()
    )
    return ConversationHandler.END


# 🚀 FUNCIÓN PRINCIPAL: Orquestador del Bot
def main() -> None:
    application = Application.builder().token(TOKEN).build()

    # Configuración de la Máquina de Estados (Control de la Conversación)
    cajero_conv = ConversationHandler(
        entry_points=[CommandHandler("start", start)],
        states={
            INGRESAR_ID: [MessageHandler(filters.TEXT & ~filters.COMMAND, validar_id)],
            MENU_PRINCIPAL: [
                MessageHandler(filters.Regex('^Cargar saldo$'), iniciar_deposito),
                MessageHandler(filters.Regex('^Retirar ganancias$'), iniciar_retiro),
                MessageHandler(filters.Regex('^Salir$'), salir),
            ],
            PROCESAR_DEPOSITO: [MessageHandler(filters.TEXT & ~filters.COMMAND, ejecutar_deposito)],
            PROCESAR_RETIRO: [MessageHandler(filters.TEXT & ~filters.COMMAND, ejecutar_retiro)],
        },
        fallbacks=[CommandHandler("start", start)],
    )

    application.add_handler(cajero_conv)
    
    print("Bot del Casino iniciado con todas las reglas de negocio... Control+C para apagar.")
    application.run_polling()

if __name__ == '__main__':
    main()
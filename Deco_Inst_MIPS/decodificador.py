# Diccionario para las instrucciones tipo R 
INSTRUCCIONES_R = {
    'ADD': {'opcode': 0b000000, 'funct': 0b100000},  # 32 en decimal
    'SUB': {'opcode': 0b000000, 'funct': 0b100010},  # 34 en decimal
    'OR':  {'opcode': 0b000000, 'funct': 0b100101}   # 37 en decimal
}

def limpiar_linea(linea):
    """
    Limpia la línea: quita comentarios, espacios extras y convierte a mayúsculas
    """
    if '#' in linea:
        linea = linea.split('#')[0]  # Quita todo después del #
    return linea.strip().upper()

def extraer_registro(registro):
    """
    Convierte $10 en 10, $t0 en 8, etc.
    Solo implemento números por simplicidad, pero puedes extenderlo
    """
    # Quita el $ y convierte a número
    registro = registro.replace('$', '')
    
    # Si es un número directo como $10
    if registro.isdigit():
        return int(registro)
    
    # Si es un registro con nombre como $t0, $s0, etc.
    # (Para futuras extensiones)
    registros_nombrados = {
        'ZERO': 0, 'AT': 1, 'V0': 2, 'V1': 3, 'A0': 4, 'A1': 5, 'A2': 6, 'A3': 7,
        'T0': 8, 'T1': 9, 'T2': 10, 'T3': 11, 'T4': 12, 'T5': 13, 'T6': 14, 'T7': 15,
        'S0': 16, 'S1': 17, 'S2': 18, 'S3': 19, 'S4': 20, 'S5': 21, 'S6': 22, 'S7': 23,
        'T8': 24, 'T9': 25, 'K0': 26, 'K1': 27, 'GP': 28, 'SP': 29, 'FP': 30, 'RA': 31
    }
    
    if registro in registros_nombrados:
        return registros_nombrados[registro]
    
    raise ValueError(f"Registro no válido: ${registro}")

def decodificar_instruccion_r(linea):
    """
    Decodifica instrucciones tipo R: ADD $rd, $rs, $rt
    Formato: [opcode 6b][rs 5b][rt 5b][rd 5b][shamt 5b][funct 6b] = 32 bits
    """
    linea_limpia = limpiar_linea(linea)
    if not linea_limpia:
        return None
    
    partes = linea_limpia.split()
    if len(partes) < 4:
        raise ValueError(f"Instrucción incompleta: {linea}")
    
    mnemonic = partes[0]
    if mnemonic not in INSTRUCCIONES_R:
        raise ValueError(f"Instrucción no soportada: {mnemonic}")
    
    # Extraer operandos: "ADD $10, $3, $4" -> rd=10, rs=3, rt=4
    # Quitamos comas y espacios
    operandos = [op.replace(',', '').strip() for op in partes[1:4]]
    
    rd = extraer_registro(operandos[0])
    rs = extraer_registro(operandos[1])
    rt = extraer_registro(operandos[2])
    
    # Validar que los registros estén entre 0-31
    for reg, nombre in zip([rd, rs, rt], ['rd', 'rs', 'rt']):
        if reg < 0 or reg > 31:
            raise ValueError(f"Registro {nombre} fuera de rango: {reg}")
    
    # Obtener datos de la instrucción
    inst_data = INSTRUCCIONES_R[mnemonic]
    
    # CONSTRUIR LA INSTRUCCIÓN DE 32 BITS
    # Formato R: opcode(6) | rs(5) | rt(5) | rd(5) | shamt(5) | funct(6)
    instruccion_bin = 0
    
    # Opcode (bits 31-26)
    instruccion_bin |= (inst_data['opcode'] & 0x3F) << 26
    # rs (bits 25-21)
    instruccion_bin |= (rs & 0x1F) << 21
    # rt (bits 20-16)
    instruccion_bin |= (rt & 0x1F) << 16
    # rd (bits 15-11)
    instruccion_bin |= (rd & 0x1F) << 11
    # shamt - siempre 0 para nuestras instrucciones (bits 10-6)
    instruccion_bin |= (0 & 0x1F) << 6
    # funct (bits 5-0)
    instruccion_bin |= (inst_data['funct'] & 0x3F)
    
    return instruccion_bin

def instruccion_a_bytes_big_endian(instruccion_bin):
    """
    Convierte una instrucción de 32 bits a 4 bytes en orden Big Endian
    Big Endian: Byte más significativo primero
    """
    bytes_resultado = []
    
    # Extraer los 4 bytes en orden Big Endian
    for i in range(4):
        # Desplazamos para obtener cada byte
        byte = (instruccion_bin >> (24 - i * 8)) & 0xFF
        bytes_resultado.append(byte)
    
    return bytes_resultado

def decodificar_archivo(contenido):
    """
    Procesa todo el contenido de un archivo y devuelve:
    - Lista de líneas originales
    - Lista de instrucciones en binario
    - Lista de bytes para el archivo de salida
    """
    lineas_originales = []
    instrucciones_bin = []
    todos_bytes = []
    
    lineas = contenido.split('\n')
    
    for linea in lineas:
        linea_limpia = limpiar_linea(linea)
        if not linea_limpia:
            continue
            
        lineas_originales.append(linea)
        
        try:
            # Decodificar la instrucción
            instruccion = decodificar_instruccion_r(linea_limpia)
            if instruccion is not None:
                instrucciones_bin.append(instruccion)
                
                # Convertir a bytes Big Endian
                bytes_inst = instruccion_a_bytes_big_endian(instruccion)
                todos_bytes.extend(bytes_inst)
                
        except Exception as e:
            # Si hay error, agregamos None para mantener el orden
            instrucciones_bin.append(None)
            print(f"Error en línea: {linea} - {e}")
    
    return lineas_originales, instrucciones_bin, todos_bytes
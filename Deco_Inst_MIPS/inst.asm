# ===============================================
# Archivo de prueba para Decodificador MIPS
# Instrucciones Tipo R - Formato: OP $rd, $rs, $rt  
# ===============================================

# Operaciones aritméticas básicas
ADD $10, $3, $4     # $10 = $3 + $4
SUB $8, $8, $9      # $8 = $8 - $9
OR $2, $2, $1       # $2 = $2 OR $1

# Más ejemplos con diferentes registros
ADD $15, $12, $13   # $15 = $12 + $13
SUB $7, $5, $6      # $7 = $5 - $6
OR $11, $14, $16    # $11 = $14 OR $16

# Operaciones con registros bajos
ADD $1, $2, $3      # $1 = $2 + $3
SUB $4, $5, $6      # $4 = $5 - $6
OR $7, $8, $9       # $7 = $8 OR $9

# Ejemplos con registros consecutivos
ADD $17, $18, $19   # $17 = $18 + $19
SUB $20, $21, $22   # $20 = $21 - $22
OR $23, $24, $25    # $23 = $24 OR $25

# Línea con espacios extras
ADD   $10,  $3,  $4     # Con múltiples espacios

# Esto es un comentario largo que debe ser ignorado
# por el decodificador, solo procesa las instrucciones válidas

# Operaciones finales
ADD $26, $27, $28   # $26 = $27 + $28
SUB $29, $30, $31   # $29 = $30 - $31
OR $0, $1, $2       # $0 = $1 OR $2 (aunque $0 es read-only)

# ===============================================
# Fin del archivo de prueba
# Total: 15 instrucciones válidas para decodificar
# ===============================================
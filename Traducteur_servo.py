# Soumettez ce fichier via Brightspace
# Ne modifiez pas la signature de la fonction.

def traduit(angle: float) -> int:
    """
    Convertit un angle en degrés vers l'entrée correspondante
    pour la méthode duty_u16 de la classe servo

    Voir https://docs.micropython.org/en/latest/library/machine.PWM.html pour plus
    de détails sur la méthode duty_u16
    """

    # Verifie que l'angle respecte les limites
    if angle < 0:
        angle = 0
    elif angle > 180:
        angle = 180

    # Calcul de la largeur d'impulsion en microsecondes
    largeur_impulsion = 500 + (2500 - 500) * (angle / 180)

    # Conversion en rapport cyclique (0–1) 
    cycle = largeur_impulsion / 20000  # 20 000 µs = 1 période (50 Hz)

    # Conversion en valeur 16 bits pour duty_u16
    duty = int(cycle * 65535)

    return duty

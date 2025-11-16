# Lire un fichier G-code et contrôler deux servos (épaule et coude)

from machine import Pin, PWM
import time

# Fonction de conversion angle → duty cycle
def traduit(angle: float) -> int:
    """
    Convertit un angle (0–180°) en valeur duty_u16 pour un servo standard.
    """
    MIN = 1638   # 0°
    MAX = 8192   # 180°
    DEG = (MAX - MIN) / 180
    angle = max(0, min(180, angle))
    return int(angle * DEG + MIN)


# Classe Servo (simplifiée grâce à traduit)
class Servo:
    def __init__(self, pin):
        self.pwm = PWM(Pin(pin))
        self.pwm.freq(50)

    def write_angle(self, angle):
        self.pwm.duty_u16(traduit(angle))
        time.sleep(0.1)

    def off(self):
        self.pwm.deinit()


# Lecture et exécution du G-code
def lire_gcode(fichier_gcode, servo_epaule, servo_coude):
    with open(fichier_gcode, "r") as f:
        for ligne in f:
            ligne = ligne.strip()
            if not ligne or ligne.startswith("#"):
                continue

            print(f"\nCommande : {ligne}")

            if ligne.startswith("G1"):
                mots = ligne.split()
                angle_epaule = None
                angle_coude = None

                for m in mots:
                    if m.startswith("S"):
                        angle_epaule = float(m[1:])
                    elif m.startswith("E"):
                        angle_coude = float(m[1:])

                if angle_epaule is not None:
                    servo_epaule.write_angle(angle_epaule)
                if angle_coude is not None:
                    servo_coude.write_angle(angle_coude)

            elif ligne.startswith("M18"):
                print("Servos désactives")
                servo_epaule.off()
                servo_coude.off()
                break


# Programme principal
if __name__ == "__main__":
    print("Traceur G-code\n")

    servo_epaule = Servo(26)
    servo_coude = Servo(27)

    # Lecture de la calibration initiale (si disponible)
    try:
        with open("calibration_init.txt", "r") as f:
            alpha_init, beta_init = map(float, f.readline().split())
            print(f"Calibration lue : Épaule={alpha_init}°, Coude={beta_init}°")
    except OSError:
        alpha_init, beta_init = 90, 90
        print("Pas de calibration trouvee, position par defaut (90°, 90°).")

    servo_epaule.write_angle(alpha_init)
    servo_coude.write_angle(beta_init)
    time.sleep(1)

    # Lecture du G-code
    lire_gcode("square.gcode", servo_epaule, servo_coude)
    print("\nDessin termine.")

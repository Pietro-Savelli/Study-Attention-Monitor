

class EyeAnalyzer:

    def __init__(self):
        self.soglia_sx = 0.60 
        self.soglia_dx = 0.40
        self.soglia_basso = 0.55

    def where_look(self, punti):
        if not punti:
            return False #non trovo gli occhi e di conseguenza non guardo lo schermo

        occhio_est = punti[33].x 
        occhio_int = punti[133].x
        pupilla = punti[468].x
        posizione_relativa_x = (pupilla - occhio_est) / (occhio_int - occhio_est)

        palpebra_su = punti[159].y
        palpebra_giu = punti[145].y
        pupilla_y = punti[468].y
        posizione_relativa_y = (pupilla_y - palpebra_su) / (palpebra_giu - palpebra_su)



        if posizione_relativa_y > self.soglia_basso:
            return False
        if posizione_relativa_x > self.soglia_sx:
            return False
        if posizione_relativa_x < self.soglia_dx:
            return False
        return True
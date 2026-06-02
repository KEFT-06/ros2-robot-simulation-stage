#!/usr/bin/env python3
"""
Script de validation de la cinématique du robot ATAWI-3A3
Teste la cinématique directe (FK) et inverse (IK) du robot
"""

import numpy as np
import math
from typing import Tuple, List

class RobotKinematics:
    """Classe pour calculer la cinématique du robot ATAWI-3A3"""
    
    def __init__(self):
        """
        Initialise les paramètres DH (Denavit-Hartenberg) du robot
        Configuration: Rotation base (0,0,1) -> Flexion bras (0,1,0) -> Rotation poignet (0,0,1)
        """
        # Longueurs des segments (en mètres)
        self.L1 = 0.2  # Longueur premier segment
        self.L2 = 0.2  # Longueur deuxième segment
        self.L3 = 0.1  # Longueur troisième segment
        
        # Limites articulaires (en radians)
        self.q_min = [-math.pi, -math.pi/2, -math.pi]
        self.q_max = [math.pi, math.pi/2, math.pi]
    
    def forward_kinematics(self, q: List[float]) -> Tuple[np.ndarray, np.ndarray]:
        """
        Calcule la cinématique directe du robot
        
        Args:
            q: Vecteur des angles articulaires [q1, q2, q3] en radians
            
        Returns:
            position: Vecteur position (x, y, z) de l'effecteur final
            orientation: Matrice de rotation 3x3
        """
        q1, q2, q3 = q
        
        # Vérifier les limites
        for i, (qi, q_min, q_max) in enumerate(zip(q, self.q_min, self.q_max)):
            if not (q_min <= qi <= q_max):
                print(f"⚠️ Avertissement: q{i+1} = {math.degrees(qi):.2f}° dépasse les limites "
                      f"[{math.degrees(q_min):.2f}°, {math.degrees(q_max):.2f}°]")
        
        # Calculs intermédiaires
        c1, s1 = math.cos(q1), math.sin(q1)
        c2, s2 = math.cos(q2), math.sin(q2)
        c3, s3 = math.cos(q3), math.sin(q3)
        
        # Position de l'effecteur final
        # Selon la structure : base -> rotation Z -> segment1 -> flexion Y -> segment2 -> rotation Z -> segment3
        x = (self.L1 + self.L2 * c2 + self.L3 * (c2 * c3 - s2 * s3 * 0)) * c1
        y = (self.L1 + self.L2 * c2 + self.L3 * (c2 * c3 - s2 * s3 * 0)) * s1
        z = self.L2 * s2 + self.L3 * (s2 * c3 + c2 * s3 * 0)
        
        position = np.array([x, y, z])
        
        # Matrice de rotation (orientation de l'effecteur)
        # Composition des rotations: Rz(q1) * Ry(q2) * Rz(q3)
        R1 = np.array([
            [c1, -s1, 0],
            [s1, c1, 0],
            [0, 0, 1]
        ])
        
        R2 = np.array([
            [c2, 0, s2],
            [0, 1, 0],
            [-s2, 0, c2]
        ])
        
        R3 = np.array([
            [c3, -s3, 0],
            [s3, c3, 0],
            [0, 0, 1]
        ])
        
        orientation = R1 @ R2 @ R3
        
        return position, orientation
    
    def inverse_kinematics_numerical(self, target_pos: np.ndarray, 
                                     q_init: List[float] = None,
                                     tolerance: float = 1e-3,
                                     max_iterations: int = 100) -> Tuple[List[float], bool]:
        """
        Calcule la cinématique inverse en utilisant la méthode Jacobienne
        
        Args:
            target_pos: Position cible [x, y, z]
            q_init: Angles initiaux (par défaut: au centre des limites)
            tolerance: Tolérance d'erreur
            max_iterations: Nombre maximum d'itérations
            
        Returns:
            q_solution: Angles solution
            success: Booléen indiquant le succès
        """
        if q_init is None:
            q_init = [(self.q_min[i] + self.q_max[i]) / 2 for i in range(3)]
        
        q = np.array(q_init, dtype=float)
        alpha = 0.01  # Pas d'apprentissage
        
        for iteration in range(max_iterations):
            # Cinématique directe actuelle
            pos_current, _ = self.forward_kinematics(q)
            
            # Erreur
            error = target_pos - pos_current
            error_norm = np.linalg.norm(error)
            
            if error_norm < tolerance:
                return q.tolist(), True
            
            # Jacobienne numérique
            J = np.zeros((3, 3))
            delta_q = 1e-5
            
            for i in range(3):
                q_plus = q.copy()
                q_plus[i] += delta_q
                pos_plus, _ = self.forward_kinematics(q_plus)
                
                J[:, i] = (pos_plus - pos_current) / delta_q
            
            # Pseudo-inverse
            try:
                J_inv = np.linalg.pinv(J)
            except np.linalg.LinAlgError:
                return q.tolist(), False
            
            # Mise à jour
            q += alpha * J_inv @ error
            
            # Respecter les limites
            for i in range(3):
                q[i] = np.clip(q[i], self.q_min[i], self.q_max[i])
        
        return q.tolist(), False
    
    def print_configuration(self, q: List[float]):
        """Affiche la configuration d'une articulation"""
        print(f"\n{'='*60}")
        print("CONFIGURATION ARTICULAIRE")
        print(f"{'='*60}")
        joint_names = ["Joint 1 (Rotation base)", "Joint 2 (Flexion bras)", "Joint 3 (Rotation poignet)"]
        for i, (qi, name) in enumerate(zip(q, joint_names)):
            deg = math.degrees(qi)
            q_min_deg = math.degrees(self.q_min[i])
            q_max_deg = math.degrees(self.q_max[i])
            print(f"{name:30s}: {deg:7.2f}° [{q_min_deg:7.2f}°, {q_max_deg:7.2f}°]")
        
        # Cinématique directe
        pos, orient = self.forward_kinematics(q)
        print(f"\n{'POSITION DE L\'EFFECTEUR':^60}")
        print(f"  X: {pos[0]:.4f} m")
        print(f"  Y: {pos[1]:.4f} m")
        print(f"  Z: {pos[2]:.4f} m")
        print(f"  Distance de l'origine: {np.linalg.norm(pos):.4f} m")
        
        print(f"\n{'MATRICE DE ROTATION':^60}")
        for row in orient:
            print(f"  [{row[0]:7.4f} {row[1]:7.4f} {row[2]:7.4f}]")


def main():
    """Test de cinématique"""
    print("\n" + "="*60)
    print("   VALIDATION CINÉMATIQUE - ROBOT ATAWI-3A3")
    print("="*60)
    
    robot = RobotKinematics()
    
    # Test 1: Configuration zéro
    print("\n[TEST 1] Configuration zéro")
    q_zero = [0, 0, 0]
    robot.print_configuration(q_zero)
    
    # Test 2: Configuration d'étirement maximal
    print("\n[TEST 2] Configuration d'étirement maximal")
    q_stretched = [0, 0, 0]
    robot.print_configuration(q_stretched)
    
    # Test 3: Configuration arbitraire
    print("\n[TEST 3] Configuration arbitraire")
    q_arbitrary = [math.pi/4, -math.pi/4, math.pi/6]
    robot.print_configuration(q_arbitrary)
    
    # Test 4: Cinématique inverse
    print("\n[TEST 4] Cinématique inverse - Cible: (0.3, 0.0, 0.2)")
    target = np.array([0.3, 0.0, 0.2])
    q_solution, success = robot.inverse_kinematics_numerical(target)
    
    if success:
        print("✅ Solution trouvée!")
        robot.print_configuration(q_solution)
        
        # Vérification
        pos_verify, _ = robot.forward_kinematics(q_solution)
        error = np.linalg.norm(target - pos_verify)
        print(f"\n✓ Erreur de vérification: {error:.6f} m")
    else:
        print("❌ Pas de solution trouvée dans les limites")
    
    print("\n" + "="*60)


if __name__ == "__main__":
    main()

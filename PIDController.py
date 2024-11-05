class PIDController:
    def __init__(self, kp, ki, kd, avg_speed, move_function):
        """
        Inicializa el controlador PID.
        :param kp: Constante proporcional.
        :param ki: Constante integral.
        :param kd: Constante derivativa.
        :param avg_speed: Velocidad promedio.
        :param move_function: Función para moverse hacia adelante.
        """
        self.kp = kp
        self.ki = ki
        self.kd = kd
        self.avg_speed = avg_speed
        self.move_function = move_function  # Función de movimiento
        self.integral = 0  # Acumulación del error para el término integral
        self.prev_error = 0  # Error anterior para el término derivativo

    def calculate(self, ir_values: list[int]) -> None:
        """
        Calcula el ajuste de velocidad basado en los valores del sensor IR.
        :param ir_values: Lista de valores IR.
        """
        # Dividir los valores de los sensores IR en izquierda y derecha
        mid = len(ir_values) // 2
        IzqIR = ir_values[0:mid]  # Sensores de la izquierda
        DerIR = ir_values[mid:]   # Sensores de la derecha

        # Cálculo del error (puedes ajustar esto según cómo quieres definir el error)
        error = sum(DerIR) - sum(IzqIR)  # Diferencia entre los lados

        # Cálculo del término integral
        self.integral += error

        # Cálculo del término derivativo
        derivative = error - self.prev_error

        # Cálculo de la salida del controlador PID
        u = (self.kp * error) + (self.ki * self.integral) + (self.kd * derivative)

        # Actualizar el error previo
        self.prev_error = error

        # Llamar a la función de movimiento con las velocidades ajustadas
        left_speed = int(self.avg_speed + u)
        right_speed = int(self.avg_speed - u)
        self.move_function(left_speed, right_speed)

        # Mostrar el error actual y el ajuste de velocidad
        print(f"Error: {error}, Ajuste: {u}, Velocidad Izq: {left_speed}, Velocidad Der: {right_speed}")
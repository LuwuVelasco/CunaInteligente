<?php
// Configuración de la conexión a la base de datos
$servername = "localhost";
$username = "root";           // Cambia esto por tu usuario de MySQL
$password = "";               // Cambia esto por tu contraseña de MySQL
$dbname = ""; // Nombre de la base de datos

try {
    // Crear conexión a la base de datos
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    // Configuración para manejar excepciones
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Verificar el método HTTP
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // Leer el contenido de la solicitud POST
        $json = file_get_contents('php://input');
        $data = json_decode($json, true);

        // Verificar que los datos JSON contengan las claves necesarias
        if (isset($data['fecha'], $data['tiempoLlanto'], $data['temperaturaActual'], $data['movimientoCuna'], $data['humedad'], $data['ultimaComida'])) {
            // Preparar la consulta SQL para inserción
            $stmt = $conn->prepare("INSERT INTO registroLLanto (fecha, tiempoLlanto, temperaturaActual, movimientoCuna, humedad, ultimaComida)
                                    VALUES (:fecha, :tiempoLlanto, :temperaturaActual, :movimientoCuna, :humedad, :ultimaComida)");

            // Enlazar los valores con los parámetros de la consulta
            $stmt->bindParam(':fecha', $data['fecha']);
            $stmt->bindParam(':tiempoLlanto', $data['tiempoLlanto']);
            $stmt->bindParam(':temperaturaActual', $data['temperaturaActual']);
            $stmt->bindParam(':movimientoCuna', $data['movimientoCuna']);
            $stmt->bindParam(':humedad', $data['humedad']);
            $stmt->bindParam(':ultimaComida', $data['ultimaComida']);

            // Ejecutar la consulta
            if ($stmt->execute()) {
                echo json_encode(["message" => "Datos insertados exitosamente"]);
            } else {
                echo json_encode(["message" => "Error al insertar los datos"]);
            }
        } else {
            echo json_encode(["message" => "Datos incompletos en el JSON recibido"]);
        }
    } elseif ($_SERVER['REQUEST_METHOD'] === 'GET') {
        // Preparar la consulta SQL para leer datos
        $stmt = $conn->prepare("SELECT * FROM registroLLanto");
        $stmt->execute();

        // Obtener los resultados
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Devolver los resultados en formato JSON
        echo json_encode($result);
    } else {
        echo json_encode(["message" => "Método HTTP no soportado"]);
    }

} catch (PDOException $e) {
    echo json_encode(["error" => "Error en la conexión: " . $e->getMessage()]);
}

// Cerrar la conexión
$conn = null;
?>

<?php
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
        if (isset($data['fecha'], $data['tiempoHumedad'], $data['horaUltimaComida'])) {
            // Preparar la consulta SQL para inserción
            $stmt = $conn->prepare("INSERT INTO registroHumedad (fecha, tiempoHumedad, horaUltimaComida)
                                    VALUES (:fecha, :tiempoHumedad, :horaUltimaComida)");

            // Enlazar los valores con los parámetros de la consulta
            $stmt->bindParam(':fecha', $data['fecha']);
            $stmt->bindParam(':tiempoHumedad', $data['tiempoHumedad']);
            $stmt->bindParam(':horaUltimaComida', $data['horaUltimaComida']);

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
        $stmt = $conn->prepare("SELECT * FROM registroHumedad");
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

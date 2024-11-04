<?php
$servername = "localhost";
$username = "root";           // Cambia esto por tu usuario de MySQL
$password = "";               // Cambia esto por tu contraseña de MySQL
$dbname = "";     // Cambia esto por el nombre de tu base de datos

try {
    // Crear conexión a la base de datos
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    // Verificar el método de solicitud
    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        // Leer el contenido de la solicitud POST
        $json = file_get_contents('php://input');
        $data = json_decode($json, true);

        // Verificar que los datos JSON contengan las claves necesarias
        if (isset($data['usuario'], $data['contraseña'])) {
            // Preparar la consulta SQL para insertar datos
            $stmt = $conn->prepare("INSERT INTO usuario (usuario, contraseña) VALUES (:usuario, :contraseña)");

            // Enlazar los valores con los parámetros de la consulta
            $stmt->bindParam(':usuario', $data['usuario']);
            $stmt->bindParam(':contraseña', $data['contraseña']);

            // Ejecutar la consulta
            if ($stmt->execute()) {
                echo json_encode(["message" => "Usuario insertado exitosamente"]);
            } else {
                echo json_encode(["message" => "Error al insertar el usuario"]);
            }
        } else {
            echo json_encode(["message" => "Datos incompletos en el JSON recibido"]);
        }
    } elseif ($_SERVER['REQUEST_METHOD'] === 'GET') {
        // Preparar la consulta SQL para leer datos
        $stmt = $conn->prepare("SELECT id_usuario, usuario FROM usuario");
        $stmt->execute();

        // Obtener los resultados
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Verificar si se encontraron resultados
        if ($result) {
            echo json_encode($result);
        } else {
            echo json_encode(["message" => "No se encontraron usuarios"]);
        }
    } else {
        echo json_encode(["message" => "Método no permitido"]);
    }
} catch (PDOException $e) {
    echo json_encode(["error" => "Error en la conexión: " . $e->getMessage()]);
}

// Cerrar la conexión
$conn = null;
?>

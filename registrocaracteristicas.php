<?php
$servername = "localhost";
$username = "root";         
$password = "";               
$dbname = "cunainteligente";    

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
        if (isset($data['id_registroCaracteristicas'], $data['fecha'], $data['peso'], $data['altura'], $data['bebe_id_bebe'])) {
            // Preparar la consulta SQL para insertar datos
            $stmt = $conn->prepare("INSERT INTO registroCaracteristicas (id_registroCaracteristicas, fecha, peso, altura, bebe_id_bebe) 
                                    VALUES (:id_registroCaracteristicas, :fecha, :peso, :altura, :bebe_id_bebe)");

            // Enlazar los valores con los parámetros de la consulta
            $stmt->bindParam(':id_registroCaracteristicas', $data['id_registroCaracteristicas'], PDO::PARAM_INT);
            $stmt->bindParam(':fecha', $data['fecha']);
            $stmt->bindParam(':peso', $data['peso']);
            $stmt->bindParam(':altura', $data['altura']);
            $stmt->bindParam(':bebe_id_bebe', $data['bebe_id_bebe'], PDO::PARAM_INT);

            // Ejecutar la consulta
            if ($stmt->execute()) {
                echo json_encode(["message" => "Datos de registro de características insertados exitosamente"]);
            } else {
                echo json_encode(["message" => "Error al insertar los datos de registro de características"]);
            }
        } else {
            echo json_encode(["message" => "Datos incompletos en el JSON recibido"]);
        }
    } elseif ($_SERVER['REQUEST_METHOD'] === 'GET') {
        // Preparar la consulta SQL para leer datos
        $stmt = $conn->prepare("SELECT id_registroCaracteristicas, fecha, peso, altura, bebe_id_bebe FROM registroCaracteristicas");
        $stmt->execute();

        // Obtener los resultados
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        // Verificar si se encontraron resultados
        if ($result) {
            echo json_encode($result);
        } else {
            echo json_encode(["message" => "No se encontraron datos de registro de características"]);
        }
    } else {
        echo json_encode(["message" => "Método no permitido"]);
    }
} catch (PDOException $e) {
    echo json_encode(["error" => "Error en la conexión: " . $e->getMessage()]);
}

$conn = null;
?>

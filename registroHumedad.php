<?php
// Configuración de la conexión a la base de datos
$servername = "localhost";
$username = "root";           // Cambia esto por tu usuario de MySQL
$password = "";               // Cambia esto por tu contraseña de MySQL
$dbname = "cunainteligente";     // Cambia esto por el nombre de tu base de datos

try {
    // Crear conexión a la base de datos
    $conn = new PDO("mysql:host=$servername;dbname=$dbname", $username, $password);
    $conn->setAttribute(PDO::ATTR_ERRMODE, PDO::ERRMODE_EXCEPTION);

    if ($_SERVER['REQUEST_METHOD'] === 'POST') {
        $json = file_get_contents('php://input');
        $data = json_decode($json, true);

        if (isset($data['humedad'], $data['fecha'], $data['cuna_id_cuna'])) {
            $stmt = $conn->prepare("INSERT INTO registroHumedad (id_registroHumedad, humedad, fecha, cuna_id_cuna) 
                                    VALUES (:id_registroHumedad, :humedad, :fecha, :cuna_id_cuna)");

            $stmt->bindParam(':id_registroHumedad', $data['id_registroHumedad'], PDO::PARAM_INT);
            $stmt->bindParam(':humedad', $data['humedad']);
            $stmt->bindParam(':fecha', $data['fecha']);
            $stmt->bindParam(':cuna_id_cuna', $data['cuna_id_cuna'], PDO::PARAM_INT);

            if ($stmt->execute()) {
                echo json_encode(["message" => "Datos de registro de humedad insertados exitosamente"]);
            } else {
                echo json_encode(["message" => "Error al insertar los datos de registro de humedad"]);
            }
        } else {
            echo json_encode(["message" => "Datos incompletos en el JSON recibido"]);
        }
    } elseif ($_SERVER['REQUEST_METHOD'] === 'GET') {
        $stmt = $conn->prepare("SELECT id_registroHumedad, humedad, fecha, cuna_id_cuna FROM registroHumedad");
        $stmt->execute();
        $result = $stmt->fetchAll(PDO::FETCH_ASSOC);

        if ($result) {
            echo json_encode($result);
        } else {
            echo json_encode(["message" => "No se encontraron datos de registro de humedad"]);
        }
    } else {
        echo json_encode(["message" => "Método no permitido"]);
    }
} catch (PDOException $e) {
    echo json_encode(["error" => "Error en la conexión: " . $e->getMessage()]);
}

$conn = null;
?>

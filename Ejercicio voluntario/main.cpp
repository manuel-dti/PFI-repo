#include <iostream>
#include <fstream>
#include <cstring>
using namespace std;
const int MAX_ALUMNOS = 50;
const int MAX_LONGITUD_NOMBRE = 250;

int main() {
    const char* archivoEntrada = "alumnos.txt";
    const char* archivoSalida = "hoja_asistencia.txt";
    char alumnos[MAX_ALUMNOS][MAX_LONGITUD_NOMBRE];
    int cantidad=0;

    ifstream archivo(archivoEntrada);
    if (archivo.fail()) {
        cerr << "Error al abrir el fichero." << endl;
        return 1;
    }

    while (cantidad < MAX_ALUMNOS && archivo.getline(alumnos[cantidad], MAX_LONGITUD_NOMBRE)) {
        cantidad++;
    }
    archivo.close();

    if (cantidad == 0) {
        cerr << "No se encontraron alumnos en el fichero." << endl;
        return 1;
    }

    for (int i = 0; i < cantidad - 1; i++) {
        for (int j = 0; j < cantidad - i - 1; j++) {
            if (strcmp(alumnos[j], alumnos[j + 1]) > 0) {
                char temp[MAX_LONGITUD_NOMBRE];
                strcpy(temp, alumnos[j]);
                strcpy(alumnos[j], alumnos[j + 1]);
                strcpy(alumnos[j + 1], temp);
            }
        }
    }

    ofstream archivoSalidaStream(archivoSalida);
    if (!archivoSalidaStream.is_open()) {
        cerr << "Error al crear el archivo de asistencia." << endl;
        return 1;
    }

    archivoSalidaStream << "Asignatura: PFIS\n";
    archivoSalidaStream << "Fecha: __/__/____\n";
    archivoSalidaStream << "Semana de docencia: ____\n";
    archivoSalidaStream << "Tema: _____________\n\n";

    int contador = 0;
    for (int i = 0; i < cantidad; i++) {
        archivoSalidaStream << alumnos[i] << "\t";
        contador++;
        if (contador % 8 == 0) {
            archivoSalidaStream << "\n";
        }
    }
    archivoSalidaStream << "\n";
    archivoSalidaStream.close();

    cout << "Hoja de asistencia generada en TXT: " << archivoSalida << endl;
    return 0;
}

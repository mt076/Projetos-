package Reviprova;

import java.util.Arrays;
import java.util.List;
import java.util.Random;

public class Sistema {
    public static void main(String[] args) {
    	
        Medico medico1 = new Medico("Dr. Matheus dos Anjos", "987.654.321-00", "CRM12345", "Médico Clínico Geral");
        Medico medico2 = new Medico("Dr. Oliveira", "456.789.123-00", "CRM54321", "Médico Clínico Geral");

        List<String> doencas = Arrays.asList("Diabetes", "Hipertensão", "Asma", "Colesterol alto", "Alergia a medicamentos", "Câncer");

        Paciente paciente1 = new Paciente("João", "123.456.789-00", "Rua A, 123", 
                Arrays.asList("Diabetes", "Hipertensão"), 80.0, 1.75, "120/80", "PlanoX", Arrays.asList("Dor de cabeça", "Febre"));

        Paciente paciente2 = new Paciente("Pedro", "987.654.321-00", "Rua B, 456", 
                Arrays.asList("Asma"), 70.0, 1.65, "110/70", "PlanoY", Arrays.asList("Dificuldade para respirar"));

        Paciente paciente3 = new Paciente("Marcos", "345.678.901-00", "Rua C, 789", 
                Arrays.asList("Colesterol alto"), 90.0, 1.80, "130/85", "PlanoZ", Arrays.asList("Cansaço"));

        Paciente paciente4 = new Paciente("Apolo", "654.321.987-00", "Rua D, 321", 
                Arrays.asList("Alergia a medicamentos"), 60.0, 1.60, "120/80", "PlanoW", Arrays.asList("Dores abdominais"));

        Random random = new Random();

        String doencaAleatoria1 = doencas.get(random.nextInt(doencas.size()));
        String doencaAleatoria2 = doencas.get(random.nextInt(doencas.size()));
        String doencaAleatoria3 = doencas.get(random.nextInt(doencas.size()));
        String doencaAleatoria4 = doencas.get(random.nextInt(doencas.size()));

        Consulta consulta1 = new Consulta("02/10/2024", paciente1, medico1);
        Consulta consulta2 = new Consulta("03/10/2024", paciente2, medico2);
        Consulta consulta3 = new Consulta("04/10/2024", paciente3, medico1);
        Consulta consulta4 = new Consulta("05/10/2024", paciente4, medico2);

        consulta1.detalhesConsulta();
        System.out.println(); 
        consulta2.detalhesConsulta();
        System.out.println(); 
        consulta3.detalhesConsulta();
        System.out.println();
        consulta4.detalhesConsulta();
        
        System.out.println("-------------------------------------------------------------");
        
        paciente1.checklistExames(); 
        System.out.println("Laudo Médico do paciente1 do dia 02/10/24: " + doencaAleatoria1);
        System.out.println(); 
        
        paciente2.checklistExames();
        System.out.println("Laudo Médico do paciente2 do dia 03/10/24: " + doencaAleatoria2);
        System.out.println(); 
        
        paciente3.checklistExames(); 
        System.out.println("Laudo Médico do paciente3 do dia 04/10/24: " + doencaAleatoria3);
        System.out.println(); 
        
        paciente4.checklistExames(); 
        System.out.println("Laudo Médico do paciente4 do dia 05/10/24: " + doencaAleatoria4);
        System.out.println();
    }
}

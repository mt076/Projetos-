package Reviprova;

import java.util.List;

public class Paciente4 extends Paciente {

	    public Paciente4(String nome, String cpf, String endereco, List<String> historicoDoencas,
	                               double peso, double altura, String pressaoArterial, String planoSaude, List<String> sintomas) {
	        super(nome, cpf, endereco, historicoDoencas, peso, altura, pressaoArterial, planoSaude, sintomas);
	    }

	    public void checklistExames() {
	        System.out.println("Exames solicitados para Paciente Emergencial:");
	        System.out.println("- Tomografia");
	        System.out.println("- Raio-X");
	        System.out.println("- Exame de sangue urgente");
	    }
	}



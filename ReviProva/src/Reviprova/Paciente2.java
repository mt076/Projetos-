package Reviprova;

import java.util.List;

public class Paciente2 extends Paciente {

	    public Paciente2(String nome, String cpf, String endereco, List<String> historicoDoencas,
	                                double peso, double altura, String pressaoArterial, String planoSaude, List<String> sintomas) {
	        super(nome, cpf, endereco, historicoDoencas, peso, altura, pressaoArterial, planoSaude, sintomas);
	    }

	    public void checklistExames() {
	        System.out.println("Exames solicitados para Paciente Ambulatorial:");
	        System.out.println("- Hemograma");
	        System.out.println("- Eletrocardiograma");
	        System.out.println("- Exame de urina");
	    }
	}


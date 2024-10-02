package Reviprova;

import java.util.Arrays;
import java.util.List;
import java.util.Random;

	public class Paciente {
	    private String nome;
	    private String cpf;
	    private String endereco;
	    private List<String> historicoDoencas;
	    private double peso;
	    private double altura;
	    private String pressaoArterial;
	    private String planoSaude;
	    private List<String> sintomas;
		private String doencaAleatoria;
	
	    private static final List<String> DOENCAS = Arrays.asList("Diabetes", "Hipertensão", "Asma", 
	            "Colesterol alto", "Alergia a medicamentos", "Câncer");
	
		public Paciente(String nome, String cpf, String endereco, List<String> historicoDoencas, 
		double peso, double altura, String pressaoArterial, String planoSaude, List<String> sintomas) {
		this.nome = nome;
		this.cpf = cpf;
		this.endereco = endereco;
		this.historicoDoencas = historicoDoencas;
		this.peso = peso;
		this.altura = altura;
		this.pressaoArterial = pressaoArterial;
		this.planoSaude = planoSaude;
		this.sintomas = sintomas;		
		this.doencaAleatoria = DOENCAS.get(new Random().nextInt(DOENCAS.size()));
		}
		
		public String getNome() {
		return nome;
		}
		
		public String getDoencaAleatoria() {
		return getDoencaAleatoria();
		}
		
		public void checklistExames() {
}
}
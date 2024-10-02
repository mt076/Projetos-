package Reviprova;

	public class Consulta {
	    private String dataConsulta;
	    private Paciente paciente;
	    private Medico medico;

	    public Consulta(String dataConsulta, Paciente paciente, Medico medico) {
	        this.dataConsulta = dataConsulta;
	        this.paciente = paciente;
	        this.medico = medico;
	    }

	    public void detalhesConsulta() {
	        System.out.println("Consulta marcada para: " + dataConsulta);
	        System.out.println("Paciente: " + paciente.getNome());
	        System.out.println("Médico: " + medico.getNome() + " (Especialidade: " + medico.getEspecialidade() + ")");
	    }

		private String getDataConsulta() {
			return dataConsulta;
		}

		private void setDataConsulta(String dataConsulta) {
			this.dataConsulta = dataConsulta;
		}

		private Paciente getPaciente() {
			return paciente;
		}

		private void setPaciente(Paciente paciente) {
			this.paciente = paciente;
		}

		private Medico getMedico() {
			return medico;
		}

		private void setMedico(Medico medico) {
			this.medico = medico;
		}

	   
	}



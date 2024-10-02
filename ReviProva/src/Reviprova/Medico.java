package Reviprova;

	public class Medico {
		protected String nome;
		protected String cpf;
		protected String crm;
		protected String especialidade;

	    public Medico(String nome, String cpf, String crm, String especialidade) {
	        this.nome = nome;
	        this.cpf = cpf;
	        this.crm = crm;
	        this.especialidade = especialidade;
	    }

	    protected String getNome() {
			return nome;
		}

	    protected void setNome(String nome) {
			this.nome = nome;
		}

	    protected String getCpf() {
			return cpf;
		}

	    protected void setCpf(String cpf) {
			this.cpf = cpf;
		}

	    protected String getCrm() {
			return crm;
		}

	    protected void setCrm(String crm) {
			this.crm = crm;
		}

	    protected String getEspecialidade() {
			return especialidade;
		}

	    protected void setEspecialidade(String especialidade) {
			this.especialidade = especialidade;
		}

	
	}



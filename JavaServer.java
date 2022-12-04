import java.io.*;  
import java.net.*;
import java.util.Random; 
public class JavaServer {
    /*Função quer gera o numero aleatoria de 1 a 5 */
    public static int GenerateRandom(){
        int min = 1;       
        int max = 5;
        int random_int = (int)Math.floor(Math.random()*(max-min+1)+min);
        
        return random_int;
    }
    /*Função que escolhe a jogada a partir do numero aleatorio */
    public static String escolha(int random){
        String opcaoServer=null;
        if (random == 1){
        opcaoServer = "Pedra";
        }
        else{
            if (random == 2){
                opcaoServer = "Papel";
            }
            else {
                if (random == 3){
                    opcaoServer = "Tesoura";
                }
                else{
                    if (random == 4){
                        opcaoServer = "Lagarto";
                    }
                    else{
                        opcaoServer = "Spock";
                    }
                }
            }
        }
        return opcaoServer;
    }
    /*Função que define o ganhador */
    public static String Winner(String myChoice, String msgCliente){
        /*#Tesoura corta papel
        #Papel cobre pedra
        #Pedra esmaga lagarto
        #Lagarto envenena Spock
        #Spock esmaga (ou derrete) tesoura
        #Tesoura decapita lagarto
        #Lagarto come papel
        #Papel refuta Spock
        #Spock vaporiza pedra
        #Pedra amassa tesoura
        */
        String winner = null;
        if (myChoice.equals("Tesoura")){
            if(msgCliente.equals("Papel")){
                winner = "Servidor";
            }
            else{
                if(msgCliente.equals("Lagarto")){
                    winner = "Servidor";
                }
                else{
                    if(msgCliente.equals("Tesoura")){
                        winner = "Empate";
                    }
                    else{
                        winner = "Cliente";
                    }
                }
            }
        }
        if (myChoice.equals( "Papel")){
            if(msgCliente.equals("Pedra")){
                winner = "Servidor";
            }
            else{
                if(msgCliente.equals("Spock")){
                    winner = "Servidor";
                }
                else{
                    if(msgCliente.equals("Papel")){
                        winner = "Empate";
                    }
                    else{
                        winner = "Cliente";
                    }
                }
            }
        }
        if (myChoice.equals( "Pedra")){
            if(msgCliente.equals("Tesoura")){
                winner = "Servidor";
            }
            else{
                if(msgCliente.equals("Lagarto")){
                    winner = "Servidor";
                }
                else{
                    if(msgCliente.equals("Pedra")){
                        winner = "Empate";
                    }
                    else{
                        winner = "Cliente";
                    }
                }
            }
        }
        if (myChoice.equals( "Lagarto")){
            if(msgCliente.equals("Spock")){
                winner = "Servidor";
            }
            else{
                if(msgCliente.equals("Papel")){
                    winner = "Servidor";
                }
                else{
                    if(msgCliente.equals("Lagarto")){
                        winner = "Empate";
                    }
                    else{
                        winner = "Cliente";
                    }
                }
            }
        }
        if (myChoice.equals( "Spock")){
            if(msgCliente.equals("Tesoura")){
                winner = "Servidor";
            }
            else{
                if(msgCliente.equals("Pedra")){
                    winner = "Servidor";
                }
                else{
                    if(msgCliente.equals("Spock")){
                        winner = "Empate";
                    }
                    else{
                        winner = "Cliente";
                    }
                }
            }
        }

        return winner;
    }

    /*Função main */
    public static void main(String[] args) {
        try{ 
            /*Inicio da conexão */
            ServerSocket serverSocket = new ServerSocket(12345);
            Socket soc = serverSocket.accept();
            System.out.println("Receive new connection: " + soc.getInetAddress());
            DataOutputStream dout=new DataOutputStream(soc.getOutputStream());  
            int countClient = 0;
            int countServer = 0;
            int countEmpate = 0;
            /*Loop do sorteio da jogada e do envio e recebimento da mensagem*/
            for(int i=0;i<15;i++){
                /*Enviando e recebendo a mensagem do cliente */
                DataInputStream in = new DataInputStream(soc.getInputStream());
                int randomNum = GenerateRandom();
                String myChoice = escolha(randomNum);
                dout.writeUTF(myChoice);
                String msgCliente=(String)in.readUTF();
                /*IMPRIMIR PLACAR */
                System.out.println("Rodada "+(i+1));
                System.out.println(myChoice+" X "+msgCliente);
                String winner = Winner(myChoice, msgCliente); /*Verifica quem ganhou a rodada */
                System.out.println("Vencedor: "+ winner);
                System.out.println("-----------------------------------------------------");
                /*CONTAGEM DAS VITORIAS */
                if(winner.equals("Cliente")){
                    countClient++;
                }
                else{
                    if(winner.equals("Servidor")){
                        countServer++;
                    }
                    else{
                        countEmpate++;
                    }
                }
                
            }
        /*Printando quem é o vencedor final após as 15 rodadas*/
        if(countClient<countServer){
            System.out.println("Vencedor final foi o Servidor com "+countServer+" vitorias, "+countEmpate+" empates e "+countClient+" derrotas");
        }
        else{
            if(countClient>countServer){
                System.out.println("Vencedor final foi o Cliente com "+countClient+" vitorias, "+countEmpate+" empates e "+countServer+" derrotas");
            }
            else{
                System.out.println("Houve um empate com o Servidor tendo "+countServer+" vitorias, "+countEmpate+" empates e "+countClient+" derrotas");
            }
        }

        /*Encerrar conexão*/
        dout.flush();
        dout.close();
        soc.close();
        }
        catch(Exception e)
        {
        e.printStackTrace(); 
    }
  }
    }
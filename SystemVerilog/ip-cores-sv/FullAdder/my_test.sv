//------------------------------------------------------------------------------
// Top-level UVM test: builds the environment and runs the main sequence.
//------------------------------------------------------------------------------
class my_test extends uvm_test;
    `uvm_component_utils (my_test)

    // Testbench environment and sequence handle.
    my_env env;
    my_sequence seqnc;

    function new (string name = "my_test", uvm_component parent = null);
        super.new (name, parent);
    endfunction

    // Create environment.
    virtual function void build_phase (uvm_phase phase);
        super.build_phase (phase);
        env = my_env::type_id::create ("env", this);
    endfunction

    // Print UVM topology after build.
    virtual function void end_of_elaboration_phase (uvm_phase phase);
        uvm_top.print_topology ();
    endfunction

    // Start the main sequence with proper objection handling.
    virtual task run_phase(uvm_phase phase);
        super.run_phase(phase);
        
        seqnc = my_sequence::type_id::create("seqnc");

        phase.raise_objection(this);

        seqnc.start(env.agent.seqr);

        phase.drop_objection(this);
    endtask
endclass
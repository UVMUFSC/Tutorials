//------------------------------------------------------------------------------
// Top-level UVM test: builds the environment and runs the main sequence.
//------------------------------------------------------------------------------
class test extends uvm_test;
    `uvm_component_utils (test)

    // Testbench environment and sequence handle.
    env              m_env;
    halfadder_sequence  m_sequence;

    function new (string name = "test", uvm_component parent = null);
        super.new (name, parent);
    endfunction

    // Create environment.
    virtual function void build_phase (uvm_phase phase);
        super.build_phase (phase);
        m_env = env::type_id::create ("env", this);
    endfunction

    // Print UVM topology after build.
    virtual function void end_of_elaboration_phase (uvm_phase phase);
        uvm_top.print_topology ();
    endfunction

    // Start the main sequence with proper objection handling.
    virtual task run_phase(uvm_phase phase);
        super.run_phase(phase);
        
        m_sequence = halfadder_sequence::type_id::create("sequence");

        phase.raise_objection(this);

        m_sequence.start(m_env.m_agent.m_sequencer);

        phase.drop_objection(this);
    endtask
endclass
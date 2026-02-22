//------------------------------------------------------------------------------
// UVM sequence: generates randomized packets until coverage reaches 100%.
// Uses a global event to wait for coverage sampling completion.
//------------------------------------------------------------------------------
class my_sequence extends uvm_sequence #(pkt);
    `uvm_object_utils(my_sequence)

    // Coverage state and synchronization event.
    real current_coverage = 0;
    uvm_event cov_sampled_event;

    function new (string name = "my_sequence");
        super.new(name);
        cov_sampled_event = uvm_event_pool::get_global("cov_sampled");  
    endfunction

    // Generate packets until the coverage goal is achieved.
    virtual task body();
        pkt packet;
        while (current_coverage < 100.0) begin
            `uvm_do(packet);

             cov_sampled_event.wait_trigger();

            void'(uvm_config_db#(real)::get(null, "*", "cov_status", current_coverage));
      
            `uvm_info("SEQ", $sformatf("Status: %0.2f%%", current_coverage), UVM_LOW)
        end
    endtask


endclass
//------------------------------------------------------------------------------
// UVM sequence: generates randomized packets until coverage reaches 100%.
// Uses a global event to wait for coverage sampling completion.
//------------------------------------------------------------------------------
class my_sequence extends uvm_sequence #(pkt);
    `uvm_object_utils(my_sequence)

    // Coverage state, synchronization event and number of randomized packets. 
    real current_coverage = 0;
    uvm_event cov_sampled_event;
    int num_packets = 0;

    function new (string name = "my_sequence");
        super.new(name);
        cov_sampled_event = uvm_event_pool::get_global("cov_sampled");  
    endfunction

    // Reuse one packet so randc state is preserved across iterations.
    // With 8-bit randc input, one full cycle is 256 unique packets.
    virtual task body();
        pkt packet;
        `uvm_create(packet)
        while (current_coverage < 100.0) begin
            `uvm_rand_send(packet)

            num_packets++;

             cov_sampled_event.wait_trigger();

            void'(uvm_config_db#(real)::get(null, "*", "cov_status", current_coverage));
      
            `uvm_info("SEQ", $sformatf("Status: %0.2f%%", current_coverage), UVM_LOW)
        end
        `uvm_info("SEQ", $sformatf("Total packets sent: %0d", num_packets), UVM_LOW)
    endtask

endclass